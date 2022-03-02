from rest_framework import serializers
from .models import Movie, Review
from accounts.serializers import UserProfileSerializer


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model= Movie
        fields = (
            'id',
            'title',
            'poster_path',
            'vote_count',
            'vote_average',
            'overview',
            'release_date',
            'tmdb_id',
            'popularity',
            'like_users',
            'wish_users',
            'genres'
        )

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    # user = UserProfileSerializer()
    
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model=Movie
            fields = ('id', 'tmdb_id', 'title',)
            
    movie = MovieSerializer(read_only=True)
    # movie = MovieSerializer()
    class Meta:
        model = Review
        fields = ('id', 'user', 'movie', 'content', 'created_at', 'updated_at', 'rank')
    