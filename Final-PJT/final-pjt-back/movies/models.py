from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    tmdb_genre_id = models.IntegerField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=500)
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    release_date = models.DateField()
    tmdb_id = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    popularity = models.FloatField()
    like_users = models.ManyToManyField(User,related_name='like_movies')
    wish_users = models.ManyToManyField(User,related_name='wish_movies')

    def __str__(self):
        return self.title


class Review(models.Model):
    RATINGS = (
        (0, '☆☆☆☆☆'),
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ) # 명예훈장 치킨 한조각 먹어도 됨
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    content = models.CharField(max_length=100)
    rank = models.IntegerField(default=0, choices=RATINGS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
