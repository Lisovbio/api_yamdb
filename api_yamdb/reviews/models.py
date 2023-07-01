# import enum
# import random
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# from django.core.mail import send_mail
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from django.db import models
# Нет файла validators, откуда импорт?
# from validators import validate_username
# from settings import AUTH_USER_MODEL


# User = models.ForeignKey(settings.AUTH_USER_MODEL)
User = get_user_model()
CHARS_TO_SHOW = 15


class Category(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Titles(models.Model):
    title = models.CharField('Название произведения', max_length=200)
    year = models.IntegerField('Дата выхода')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Название',
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
        blank=True,
        null=True
    )
    description = models.TextField()

    def __str__(self):
        return self.title


ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
)


# class CustomUserManager(UserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         """
#         Создает и возвращает пользователя с email, паролем, именем
#         и отправляет confirmation code на почту для дальнейшего получения
#         jwt токена.
#         """
#         if username is None:
#             raise TypeError('Пользователь должен иметь username.')
#         if email is None:
#             raise TypeError('Пользователь должен иметь email.')
#         user = self.model(
#             username=username,
#             email=self.normalize_email(email),
#             confirmation_code=random.randint(100000000, 999999999),
#             **extra_fields,
#         )
#         user.set_password(password)
#         user.save()
#         send_mail(
#             'Ключ для вашего аккаунта',
#             f'Для получения токена воспользуйтесь ключём:'
#             f'{user.confirmation_code}',
#             'yamdb@example.com',
#             [email],
#             fail_silently=False,
#         )
#         return user

#     def create_superuser(self, username, email, password, **extra_fields):
#         """
#         Создает и возвращает суперпользователя с email, паролем, именем
#         и присваивае суперпользователю роль admin.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('role', 'admin')
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         if extra_fields.get('username') == 'me':
#             raise ValueError('Имя "me" недопускается!')
#         return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    bio = models.TextField(blank=True)

    username = models.CharField(blank=False, max_length=150,
                                unique=True)
    email = models.EmailField(blank=False, max_length=254,
                              unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='user')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ['username']


class Review(models.Model):
    text = models.TextField("место для текста")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор"
    )
    score = models.IntegerField(
        "рейтинг",
        validators=[
            MaxValueValidator(
                limit_value=10, message="Выберите число не больше 10"
            ),
            MinValueValidator(
                limit_value=1, message="Выберите число не меньше 1"
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name="произведение",
        related_name="reviews"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f'{self.text[:20]} для {self.title}'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Комментарии",
        related_name="comments"
    )

    class Meta:
        verbose_name = "Коммментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.text[:20]} для {self.review}'
