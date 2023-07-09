from rest_framework import routers
from django.urls import include, path
from api.views import create_token, create_user
from api.views import (TitleViewSet, CategoryViewSet, CommentViewSet,
                       ReviewViewSet, GenreViewSet, UsersViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(r"titles", TitleViewSet, basename="titles")
v1_router.register(r"categories", CategoryViewSet, basename="category")
v1_router.register(r"genres", GenreViewSet, basename="genre")
v1_router.register(r"users", UsersViewSet, basename="users")
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="reviews",
)

urlpatterns = [
    path("v1/auth/signup/", create_user, name="register"),
    path("v1/auth/token/", create_token, name="token"),
    path("v1/", include(v1_router.urls)),
]
