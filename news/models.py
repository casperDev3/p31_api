from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новини")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    # Optional fields for future use
    author = models.CharField(max_length=100, verbose_name="Автор", null=True)
    image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name="Зображення")
    tags = models.CharField(max_length=200, null=True, blank=True, verbose_name="Теги",
                            help_text="Введіть теги через кому")
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name="Категорія")

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва тегу")

    def __str__(self):
        return self.name
