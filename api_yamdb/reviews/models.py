from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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


class Review(models.Model):
    text = models.TextField("место для текста")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор"
    )
    score = models.IntegerField("рейтинг")
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
