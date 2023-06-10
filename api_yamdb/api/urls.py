from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

apps_name = 'api'

router = DefaultRouter()

router.register('v1/categories', CategoryViewSet, basename='categories',)
router.register('v1/genres', GenreViewSet, basename='genres')
router.register('v1/titles', TitleViewSet, basename='titles')
router.register(r'title/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
]
