import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    title_contains = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    content_contains = django_filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['id', 'tags']

class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article
        filterset_class = ArticleFilter
        interfaces = (graphene.relay.Node,)



class NewsType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_date')


class Query(graphene.ObjectType):
    article = graphene.relay.Node.Field(ArticleNode)
    filter_articles = DjangoFilterConnectionField(ArticleNode)
    all_articles = graphene.Field(NewsType)

    def resolve_all_articles(root, info):
        return Article.objects.all()