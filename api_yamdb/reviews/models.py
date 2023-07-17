from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.db import models

from .validators import validate_year, validate_username

CHARS_TO_SHOW = 15


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=settings.USERNAME_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        verbose_name='Email',
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        max_length=settings.ROLE_LENGTH,
        choices=settings.ROLE_CHOICES,
        verbose_name='Фамилия',
        default=settings.USER,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
    )
    first_name = models.CharField(
        max_length=settings.USERNAME_LENGTH,
        verbose_name='Имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=settings.USERNAME_LENGTH,
        verbose_name='Фамилия',
        null=True,
    )

    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        verbose_name='Код подтверждения',
        null=True,
        blank=False,
    )
    is_activated = models.BooleanField(
        default=False,
        verbose_name='Статус активации',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            ),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return any(
            [self.role == settings.ADMIN, self.is_superuser],
        )

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR


class Category(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'год',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


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
        Title,
        on_delete=models.CASCADE,
        verbose_name="произведение",
        related_name="reviews"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]

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
