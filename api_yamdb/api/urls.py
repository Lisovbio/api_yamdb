from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

apps_name = 'api'

router = DefaultRouter()

router.register('v1/categories', CategoryViewSet, basename='categories',)
router.register('v1/genres', GenreViewSet, basename='genres')
router.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
