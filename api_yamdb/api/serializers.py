from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Titles, User
from reviews.validators import validate_username
from reviews.models import Category, Genre, Titles, Review, Comment
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=False, write_only=True)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(r'^[\w.+-]+\Z', 'Enter a valid username.'),
            validate_username
        ],
    )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'password',
        )
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'bio': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class GetTokenSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True, max_length=256),
    confirmation_code = serializers.CharField(write_only=True),
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = self.initial_data.get('username', None)
        confirmation_code = self.initial_data.get('confirmation_code', None)
        if username is None:
            raise serializers.ValidationError(
                'Требуется username!'
            )
        if (confirmation_code is None
            or confirmation_code != get_object_or_404(
                User,
                username=username).confirmation_code):
            raise serializers.ValidationError(
                'confirmation_code некорректен!'
            )
        user = get_object_or_404(User,
                                 username=username,
                                 confirmation_code=confirmation_code)
        return {'token': user.create_jwt_token}


class RetrieveUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=254,
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя me нельзя использовать'
            )
        if User.objects.filter(username=value).exists():
            return serializers.ValidationError(
                'Пользователя с таким именем уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError(
                'Данный Email уже используется')
        return value


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя me нельзя использовать'
            )
        return value


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        user = self.context.get("request").user
        title_id = self.context.get("view").kwargs.get("title_id")
        if self.context.get("request").method == "POST":
            review = Review.objects.filter(title_id=title_id, author=user)
            if review.exists():
                raise ValidationError("Такой объект уже создан!")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_LENGTH,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ'),
        ),
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, user):
        if user.lower() == 'me':
            raise serializers.ValidationError(
                'Пользователь me не может быть создан',
            )
        return User


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)
