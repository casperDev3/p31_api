import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters import OrderingFilter
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    title_contains = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    content_contains = django_filters.CharFilter(field_name='content', lookup_expr='icontains')

    order_by = OrderingFilter(
        fields=(
            ('created_date', 'created_date'),
            ('title', 'title'),
        )
    )

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
    all_articles = graphene.List(NewsType)
    my_articles = graphene.List(NewsType)

    def resolve_all_articles(root, info):
        return Article.objects.all()

    #TODO: Implement authentication and authorization for this query
    # def resolve_my_articles(root, info):
        # user = info.context.user
        # print(user)
        # print(user.is_authenticated)
        # print(info.context)
        # if user.is_anonymous:
        #     raise Exception('You are not logged in')
        # return Article.objects.filter(author=info.context.user)