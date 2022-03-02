from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
    path('<str:username>/follow/', views.follow),
    path('<str:username>/profile/', views.get_profile),
    path('<str:username>/likemovies/', views.get_like_movies),
    path('<str:username>/watchmovies/', views.get_watch_movies),
]
