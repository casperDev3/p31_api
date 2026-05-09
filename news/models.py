from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новини")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    # Optional fields for future use
    author = models.ForeignKey(
        User,
        related_name='news',
        verbose_name='Автор',
        on_delete=models.CASCADE,  # Якщо користувач видаляється, видаляються і його статті
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

    # after creating an article, we can send a notification to all users via WebSocket
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'news_notifications',
                {
                    'type': 'send_notification',
                    'message': f'{self.title}',
                }
            )


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    news = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Новини',
        blank=True,  # Дозволяє категорії існувати без прив'язки до статей
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
