from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Category, Tag
from .serializers import ArticleSerializer, CategorySerializer, TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_date')
    serializer_class = ArticleSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['category', 'author'] # Точний фільтр за категорією та автором
    search_fields = ['title', 'content'] # Пошук за заголовком та вмістом
    ordering_fields = ['created_date', 'title'] # Сортування за датою створення та заголовком
    ordering = ['-created_date'] # За замовчуванням сортувати за датою створення у спадному порядку



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
