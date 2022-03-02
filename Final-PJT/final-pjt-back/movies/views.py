from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
from rest_framework import serializers, status
from .models import Movie, Genre, Review
from .serializers import MovieSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decouple import config
import random
from django.db.models import Q


# Create your views here.
API_KEY = config('SECRET_KEY')

@api_view(['GET'])
def get_genres_db(request):
    if Genre.objects.exists():
        pass
    else:
        url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&region=KR&language=ko'
        req = requests.get(url).json()
        Genre.objects.bulk_create(
            [Genre(
                tmdb_genre_id = data.get('id'),
                name = data.get('name'),
                ) for data in req.get('genres')]
        )
        return Response({ 'db': '장르 생성' })
    return Response({'db': '이미 Genre 데이터 있음'})

@api_view(['GET'])
def get_popular_movies_db(request):
    popular_movies = []
    for page in range(1,61):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}&region=KR&language=ko'
        datas = requests.get(url).json()
        for data in datas.get('results'):
            if Movie.objects.filter(title=data.get('title')).exists():
                movie =  Movie.objects.get(title=data.get('title'))
                movie.popularity = data.get('popularity')
                movie.vote_count = data.get('vote_count')
                movie.vote_average = data.get('vote_average')
                movie.save()
            else:
                movie = Movie.objects.create(
                    tmdb_id = data.get('id'),
                    title = data.get('title'),
                    poster_path = 'https://image.tmdb.org/t/p/w500' + data.get('poster_path'),
                    overview = data.get('overview'),
                    vote_count = data.get('vote_count'),
                    vote_average = data.get('vote_average'),
                    release_date = data.get('release_date'),
                    popularity = data.get('popularity'),
                )
                for genre_id in data.get('genre_ids'):
                    genre = Genre.objects.get(tmdb_genre_id=genre_id)
                    genre.movies.add(movie)

            popular_movies.append(movie)
    movies = popular_movies[:15]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_now_playing_movies_db(request):
    now_playings = []
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&region=KR&language=ko'
    datas = requests.get(url).json()

    for data in datas.get('results'):
        if Movie.objects.filter(title=data.get('title')).exists():
            movie =  Movie.objects.get(title=data.get('title'))
            movie.popularity = data.get('popularity')
            movie.vote_count = data.get('vote_count')
            movie.vote_average = data.get('vote_average')
            movie.save()
        else:
            movie = Movie.objects.create(
                tmdb_id = data.get('id'),
                title = data.get('title'),
                poster_path = 'https://image.tmdb.org/t/p/w500' + data.get('poster_path'),
                overview = data.get('overview'),
                vote_count = data.get('vote_count'),
                vote_average = data.get('vote_average'),
                release_date = data.get('release_date'),
                popularity = data.get('popularity'),
            )
            for genre_id in data.get('genre_ids'):
                genre = Genre.objects.get(tmdb_genre_id=genre_id)
                genre.movies.add(movie)
        now_playings.append(movie)
    serializer = MovieSerializer(now_playings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk= movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method =='GET':
        reviews = Review.objects.filter(movie_id=movie_pk)
        serializer = ReviewSerializer(reviews, many=True)
        data = serializer.data
        return Response(data)
    else:
        if movie.reviews.all().filter(user_id = request.user.id).exists():
            raise Exception("이미 댓글이 있습니다.")
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            # movie에서 moive 돼서 에러 떳었음
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'review': '생성되지 않았습니다.' })

@api_view(['GET'])
def check_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.reviews.all().filter(user_id=request.user.id).exists():
        review = movie.reviews.get(user_id=request.user.id)
        serializer = ReviewSerializer(review)
        reviewed = True
        serializers = {
            'serializer': serializer.data,
            'reviewed': reviewed
        }
        return Response(serializers)
    else:
        reviewed = False
        dumy = {'content': '없음', 'rank': 5, 'id': 1111}
        context = {
            'serializer': dumy,
            'reviewed': reviewed
        },
        return Response(context)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.user == review.user:
        if request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        elif request.method == 'DELETE':
            review.delete()
            data = {
                'delete': f'{review_pk}번 리뷰가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
    return Response({ 'Unauthorized': '권한이 없어요.' }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_similar_movies(request, movie_pk):
    similar_movies_list = []
    movie = Movie.objects.get(pk=movie_pk)
    genre = movie.genres.all()[0]
    print(genre)
    similar_movies = genre.movies.all()
    for i in range(5):
        idx = random.randint(0,len(similar_movies)-1)
        similar_movies_list.append(similar_movies[idx])
    serializer = MovieSerializer(similar_movies_list, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def likes(request, movie_pk):
    # if request.user.is_authenticated:
    movie  = get_object_or_404(Movie, pk= movie_pk)
    if request.method == 'GET':
        if movie.like_users.filter(pk = request.user.pk).exists():
            liked = False
        else:
            liked = True
        context = {
            'liked': liked,
        }
        return JsonResponse(context)
    else:
        if movie.like_users.filter(pk = request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        context = {
            'movieId': movie.id,
            'liked': liked,
        }
        return JsonResponse(context)

@api_view(['GET', 'POST'])
def watch(request, movie_pk):
    # if request.user.is_authenticated:
    movie  = get_object_or_404(Movie, pk= movie_pk)
    if request.method == 'GET':
        if movie.wish_users.filter(pk = request.user.pk).exists():
            wished = False
        else:
            wished = True
        context = {
            'wished': wished,
        }
        return JsonResponse(context)
    else:
        if movie.wish_users.filter(pk = request.user.pk).exists():
            movie.wish_users.remove(request.user)
            wished = False
        else:
            movie.wish_users.add(request.user)
            wished = True
        context = {
            'movieId': movie.id,
            'wished': wished,
        }
        return JsonResponse(context)

@api_view(['GET'])
def get_all_movies_db(request):
    movie = Movie.objects.all()
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_genre_movies(request, category):
    movies = Movie.objects.all()
    genre_movies = set()
    for movie in movies:
        for genre in movie.genres.all():
            if category ==1 : # 액션 모험 sf
                if genre.id == 1 or genre.id == 2 or genre.id == 15:
                    genre_movies.add(movie)

            elif category == 2: # 가족 코미디
                if genre.id == 8 or genre.id == 4:
                    genre_movies.add(movie)

            elif category == 3: # 드라마 로맨스
                if genre.id == 7 or genre.id == 14:
                    genre_movies.add(movie)

            elif category == 4: # 범죄 스릴러
                if genre.id == 5 or genre.id == 17:
                    genre_movies.add(movie)

            elif category == 5: # 공포 미스터리
                if genre.id == 11 or genre.id == 13:
                    genre_movies.add(movie)

            elif category == 6: # 역사 전쟁
                if genre.id == 10 or genre.id == 18 or genre.id == 19:
                    genre_movies.add(movie)

            else:
                if genre.id == 3:
                    genre_movies.add(movie)

        if len(genre_movies) == 20:
            break
    genre_movies = list(genre_movies)[:20]
    serializer = MovieSerializer(genre_movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recommended_by_like(request):
    user = request.user
    like_movies = user.like_movies.all()
    like_movies_id = []
    for like_movie in like_movies:
        like_movies_id.append(like_movie.id)
    tmp_movie_ids = []
    # 좋아하는 영화가 있는 경우
    if len(like_movies) >= 1:
        for like_movie in like_movies:
            movie = Movie.objects.get(pk=like_movie.id)
            genre = movie.genres.all()[0]
            # 비슷한 장르의 영화 중 populartiy 내림차순 정렬 후 좋아요 누른 영화 당 가장 높은 popularity를 가진 영화 20개 추가
            similar_movies = genre.movies.all().order_by('-popularity')
            cnt = 0
            for similar_movie in similar_movies:
                # 만약 이미 좋아요를 누른 영화거나 담아놓은 영화라면 pass
                if similar_movie.id in like_movies_id or similar_movie.id in tmp_movie_ids:
                    pass
                else:
                    tmp_movie_ids.append(similar_movie.id)
                    cnt += 1
                if cnt == 20:
                    break
        recommended_movies = []
        for movie_id in tmp_movie_ids:
            movie = Movie.objects.get(pk=movie_id)
            recommended_movies.append(movie)
        # 좋아하는 영화 수 X 20 개의 영화 데이터 중 10를 랜덤 뽑기 후 전송
        serializer = MovieSerializer(random.sample(recommended_movies, 10), many=True)
        return Response(serializer.data)
    else:
        # 좋아하는 영화가 없는 경우
        for i in range(5):
            # 임의로 5개의 영화를 가져온 후
            random_id = random.randint(1, len(Movie.objects.all()))
            movie = Movie.objects.get(pk = random_id)
            genre = movie.genres.all()[0]
            # 위와 같은 방식으로 임의의 영화 장르와 비슷한 영화 목록 20개씩을 받아온 후
            similar_movies = genre.movies.all().order_by('-popularity')
            cnt = 0
            for similar_movie in similar_movies:
                if similar_movie.id in tmp_movie_ids:
                    pass
                else:
                    tmp_movie_ids.append(similar_movie.id)
                    cnt += 1
                if cnt == 20:
                    break
        recommended_movies = []
        for movie_id in tmp_movie_ids:
            movie = Movie.objects.get(pk=movie_id)
            recommended_movies.append(movie)
        # 총 100개의 영화 정보 중 10개 랜덤 뽑기 후 전송
        serializer = MovieSerializer(random.sample(recommended_movies, 10), many=True)
        return Response(serializer.data)

@api_view(['GET'])
def recommended_by_rate(request):
    movies = Movie.objects.all().order_by('-vote_average', '-release_date')
    reco_movies = []
    for movie in movies:
        reco_movies.append(movie)
        if len(reco_movies) == 50:
            break
    serializer = MovieSerializer(random.sample(reco_movies, 10), many=True)
    return Response(serializer.data)