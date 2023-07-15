from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets
from django.db import IntegrityError
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title, Review, User
from api.filter import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import AdminOnly, IsAdminUserOrReadOnly, \
    AdminModeratorAuthorPermission
from .serializers import CategorySerializer, GenreSerializer, \
    TitleReadSerializer, TitleWriteSerializer, CommentSerializer, \
    ReviewSerializer, UserSerializer, GetTokenSerializer, SignUpSerializer, \
    NotAdminSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, AdminOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission, )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AdminModeratorAuthorPermission
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class GetTokenView(APIView):
    """Вьюсет для создания токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(
            User, username=serializer.validated_data['username'],
        )
        if user.is_activated:
            return Response(
                'Пользователь уже активирован.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_activated = True
        user.save()
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    """Вьюсет для регистрации."""
    permission_classes = (AllowAny,)

    def send_confirmation_code(self, user):
        confirmation_code = default_token_generator.make_token(user)
        return send_mail(
            'Код подтверждения',
            'Код подтверждения {0}'.format(confirmation_code),
            recipient_list=[user.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            fail_silently=False,
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email'),
            )
            if not created:
                if user.is_activated:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    self.send_confirmation_code(user)
                    return Response(
                        'Новый код подтверждения отправлен на вашу почту.',
                        status=status.HTTP_200_OK,
                    )
        except IntegrityError:
            return Response(
                'Имя пользователя или email уже заняты.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
