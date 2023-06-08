# Не применяется импорт
import datetime as dt

from rest_framework import serializers
<<<<<<< HEAD

from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Titles, User
# В ревью нет файла validators
from reviews.validators import validate_username
=======
from reviews.models import Category, Genre, Titles, Review, Comment
>>>>>>> reviews


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


<<<<<<< HEAD
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
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
=======
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
>>>>>>> reviews
