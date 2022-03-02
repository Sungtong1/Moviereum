from django.db import models
from django.conf import settings


# Create your models here.
class Article(models.Model):

    CATEGORY = (
    (0, 'Daily'),
    (1, 'QnA'),
    (2, 'Recommend'),
    (3, 'Review'),
    ) 

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.IntegerField(default=0, choices=CATEGORY)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model): # 대댓글 이야기 나오자 급발진
    content= models.CharField(max_length=100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content