from django.urls import path
from . import views


urlpatterns = [
    path('populars/', views.get_popular_movies_db),
    path('nowplayings/', views.get_now_playing_movies_db),
    path('<int:movie_pk>/', views.movie_detail),
    path('<int:movie_pk>/similar/', views.get_similar_movies),
    path('getgenres/', views.get_genres_db),
    path('<int:movie_pk>/reviews/', views.review_list),
    path('<int:movie_pk>/checkreview/', views.check_review),
    path('reviews/<int:review_pk>/', views.review_detail),
    path('<int:movie_pk>/likes/', views.likes),
    path('<int:movie_pk>/watch/', views.watch),
    path('all/', views.get_all_movies_db),
    path('genremovies/<int:category>/', views.get_genre_movies),
    path('recobylike/', views.recommended_by_like),
    path('recobyrate/', views.recommended_by_rate),
]
