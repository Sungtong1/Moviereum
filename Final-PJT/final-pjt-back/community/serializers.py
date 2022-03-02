from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('article',)


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ('category','id', 'user', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count')

