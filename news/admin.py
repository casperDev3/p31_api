from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Article, Category, Tag


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('created_date',)

    readonly_fields = ('created_date', 'id')
    fields = (
        'id',
        'title',
        'content',
        'created_date',
        'author',
        'image',
        'tags',
        'category'
    )


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
