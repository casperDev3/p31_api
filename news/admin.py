from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
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
