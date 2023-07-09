from rest_framework import routers
from django.urls import include, path

from api.views import (TitleViewSet, CategoryViewSet, CommentViewSet, 
                       ReviewViewSet, GenreViewSet)

v1_router = routers.DefaultRouter()

v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')
# v1_router.register('follow', FollowViewSet, basename='follow')


urlpatterns = [
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(v1_router.urls)),
]
