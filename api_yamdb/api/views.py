from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import mixins
from titles.models import Category, Genre, Title, Review, Comment

# from api.permissions import IsOwnerOrReadOnly
from api.serializers import (TitleSerializer, GenreSerializer, 
                             ReviewSerializer, CommentSerializer,
                             CategorySerializer, TitleRetrieveSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    # permission_classes = (AllowAny,)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    # permission_classes = (AllowAny,)
 


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # pagination_class = LimitOffsetPagination
    # permission_classes = (IsOwnerOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleRetrieveSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)




class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(review=review, author=self.request.user)


# class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#     permission_classes = (IsAuthenticated, )
#     filter_backends = (filters.SearchFilter, )
#     search_fields = ('following__username', 'user__username')

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.request.user.username)
#         return user.follower

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
