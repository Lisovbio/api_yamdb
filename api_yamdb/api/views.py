# from django.shortcuts import get_object_or_404
from rest_framework import viewsets   # , filters, permissions,

from reviews.models import Category, Genre, Titles
# from .permissions import IsAuthorOrReadOnly
# from .serializers import CommentSerializer, FollowSerializer, \
#     GroupSerializer, PostSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass
