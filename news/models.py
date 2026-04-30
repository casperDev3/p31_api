from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новини")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    # Optional fields for future use
    author = models.ForeignKey(
        User,
        related_name='news',
        verbose_name='Автор',
        on_delete=models.CASCADE, # Якщо користувач видаляється, видаляються і його статті
        null=True,
    )
    image = models.ImageField(upload_to='articles/%Y/%m/', null=True, blank=True, verbose_name="Зображення")
    tags = models.CharField(max_length=200, null=True, blank=True, verbose_name="Теги",
                            help_text="Введіть теги через кому")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    news = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Новини',
        blank=True, # Дозволяє категорії існувати без прив'язки до статей
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва тегу")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст коментаря")
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Стаття',
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Коментар до '{self.article.title}' від {self.author.username if self.author else 'Анонім'}"