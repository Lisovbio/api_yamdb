from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    SignUpView,
    GetTokenView
)

apps_name = 'api'


router = SimpleRouter()
router.register('v1/categories', CategoryViewSet, basename='categories',)
router.register('v1/genres', GenreViewSet, basename='genres')
router.register('v1/users', UserViewSet, basename='users')
router.register('v1/titles', TitleViewSet, basename='titles')
router.register(r'v1/titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
    path('', include(router.urls))
]
