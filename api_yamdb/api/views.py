from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


from reviews.models import Category, Genre, Titles, Review
from .permissions import IsAdminOrReadOnly, CustomPermission
from .serializers import CategorySerializer, GenreSerializer, \
    TitlesSerializer, CommentSerializer, ReviewSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title', 'year', 'category', 'genre')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
<<<<<<< HEAD
    permission_classes = (CustomPermission,)
=======
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorPermission
    ]
>>>>>>> a6d2f624574376fb2c9b3ab946b560737406a602

    def get_queryset(self):
        title = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        queryset = title.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
<<<<<<< HEAD
    permission_classes = (CustomPermission,)
=======
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorPermission
    ]
>>>>>>> a6d2f624574376fb2c9b3ab946b560737406a602

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
