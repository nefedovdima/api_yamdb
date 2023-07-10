from uuid import uuid4

from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet

from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateTokenSerializer, GenreSerializer,
                             RegistrationSerializer, ReviewSerializer,
                             TitlePostSerializer,
                             UserSerializer, TitleSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        url_path="me",
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def get_user(self, request, pk=None):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
    except IntegrityError:
        return Response(
            'Данный email уже занят',
            status=status.HTTP_400_BAD_REQUEST
        )
    if created:
        user.is_active = False
    user.confirmation_code = uuid4().hex
    user.save()
    send_mail(
        "Подтвердите регистрацию",
        f"Код подтверждения: {user.confirmation_code}",
        DEFAULT_FROM_EMAIL,
        [user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_token(request):
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(
        {"confirmation_code": "Неверный код подтверждения"},
        status=status.HTTP_400_BAD_REQUEST,
    )


class GenreViewSet(CreateListDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "slug")
    lookup_field = "slug"


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("name", "slug")
    filterset_fields = ("name", "slug")
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return (
                Title.objects.prefetch_related('reviews').all().
                annotate(rating=Avg('reviews__score')).
                order_by('name')
            )
        return Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
