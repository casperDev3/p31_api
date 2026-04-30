from rest_framework import serializers
from .models import Article, Category, Tag, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['title']
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
