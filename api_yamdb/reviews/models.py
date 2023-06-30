from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator, MinValueValidator,
)
from django.db import models
from django.contrib.auth import get_user_model


CHARS_TO_SHOW = 15
User = get_user_model()


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
