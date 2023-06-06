import enum
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.mail import send_mail
from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator,
)
from django.db import models

from .validators import regex_validator, validate_username

CHARS_TO_SHOW = 15


class Category(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()


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


class ROLE_LIST(enum.Enum):
    admin = 'admin'
    user = 'user'
    moderator = 'moderator'


class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с email, паролем, именем
        и отправляет confirmation code на почту для дальнейшего получения
        jwt токена.
        """
        if username is None:
            raise TypeError('Пользователь должен иметь username.')
        if email is None:
            raise TypeError('Пользователь должен иметь email.')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=random.randint(100000000, 999999999),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        send_mail(
            'Ключ для вашего аккаунта',
            f'Для получения токена воспользуйтесь ключём:'
            f'{user.confirmation_code}',
            'yamdb@example.com',
            [email],
            fail_silently=False,
        )
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Создает и возвращает суперпользователя с email, паролем, именем
        и присваивае суперпользователю роль admin.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('username') == 'me':
            raise ValueError('Имя "me" недопускается!')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$'), validate_username]
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        choices=[(role.value, role.name) for role in ROLE_LIST],
        max_length=10,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=9, blank=True
    )
    email = models.EmailField('Почта', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    objects = CustomUserManager()

    def create_jwt_token(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)
