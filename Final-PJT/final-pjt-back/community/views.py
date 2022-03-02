from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method=='GET':
        # articles = get_list_or_404(Article)
        articles = Article.objects.all().order_by('-pk')
        serializer = ArticleSerializer(articles, many=True)
        data = serializer.data
        return Response(data)
    else:
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'article': '생성되지 않았습니다.' })

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.user == article.user:
        if request.method == 'PUT':
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        elif request.method == 'DELETE':
            article.delete()
            data = {
                'delete': f'{article_pk}번 게시글이 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
    return Response({ 'Unauthorized': '권한이 없어요.' }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method=='GET':
        # articles = get_list_or_404(Article)
        comments = Comment.objects.filter(article_id= article_pk)
        serializer = CommentSerializer(comments, many=True)
        data = serializer.data
        return Response(data)
    else:
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'article': '생성되지 않았습니다.' })

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.user == comment.user:
        if request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        elif request.method == 'DELETE':
            comment.delete()
            data = {
                'delete': f'{comment_pk}번 리뷰가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
    return Response({ 'Unauthorized': '권한이 없어요.' }, status=status.HTTP_401_UNAUTHORIZED)