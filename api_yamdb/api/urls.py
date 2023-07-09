from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       SignUpView, GetTokenView)

apps_name = 'api'


router = DefaultRouter()
router.register('v1/users', UserViewSet, basename='users')
router.register('v1/categories', CategoryViewSet, basename='categories',)
router.register('v1/genres', GenreViewSet, basename='genres')
router.register('v1/titles', TitleViewSet, basename='titles')
router.register(r'title/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
<<<<<<< HEAD
    path('', include(router.urls)),
=======
    path('v1/', include(router.urls)),
>>>>>>> b9b0f7c97cf68603c6f2be71858c7151f969817f
]
