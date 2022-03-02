from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import User

# Create your views here.
@api_view(['GET'])
def get_profile(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserProfileSerializer(user)
    following_list = []
    follower_list = []
    for i in user.followings.all():
        following_list.append(i.username)
    for i in user.followers.all():
        follower_list.append(i.username)
    followers = user.followers.count()
    followings = user.followings.count()
    print(following_list)
    print(follower_list)
    # 태현님 작품
    serializers = {
        'serializer': serializer.data, 
        'followerCnt': followers, 
        'followingCnt': followings,
        'followings': following_list, 
        'followers' : follower_list,
        'userId': user.id,
    }
    return Response(serializers)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({ 'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def follow(request, username):
    person = get_object_or_404(get_user_model(), username=username)

    if request.user != person:
        if request.user in person.followings.all():
            followed = False
            person.followings.remove(request.user)
        else:
            followed = True
            person.followings.add(request.user)
        
        context = {
            'followed': followed,
            'person': person.username,
        }
        return JsonResponse(context)
    return Response({ 'user': '본인입니다.' })

@api_view(['GET'])
def get_like_movies(request, username):
    like_movies_list = []
    person = get_object_or_404(get_user_model(), username=username)
    like_movies = person.like_movies.all()
    for like_movie in like_movies:
        like_movies_list.append(like_movie.id)
    serializers = {
        'like_movies_list' : like_movies_list
    }
    return Response(serializers)

@api_view(['GET'])
def get_watch_movies(request, username):
    wish_movies_list = []
    person = get_object_or_404(get_user_model(), username=username)
    wish_movies = person.wish_movies.all()
    for wish_movie in wish_movies:
        wish_movies_list.append(wish_movie.id)
    serializers = {
        'wish_movies_list': wish_movies_list
    }
    return Response(serializers)



