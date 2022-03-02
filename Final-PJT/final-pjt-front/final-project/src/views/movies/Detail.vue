<template>
  <div class="detaildiv">
    <div class="container">
        <iframe v-if="videoKey" :src="videoURI" frameborder="1" style="display:block; width:100%; height: 60vh" allowfullscreen></iframe>
        <br><br>
      <div class="d-flex">
        <img :src="movieData.poster_path" alt="movie">
        <div class="ms-3">
          <h1 style="font-family: 'GowunDodum-Regular';">
            <strong>{{ movieData.title }}</strong>
          </h1>
          <div class="d-flex">
            <div v-if="!liked">
              <b-button @click="likeMovie" variant="danger" class="mt-1">
                UnLike
                <b-icon icon="suit-heart"></b-icon>
              </b-button>
            </div>
            <div v-else>
              <b-button @click="likeMovie" variant="danger" class="mt-1">
                Like
                <b-icon icon="suit-heart-fill"></b-icon>
              </b-button>
            </div>
            <div v-if="!wished" class="ms-3 mt-1">
              <b-button @click="wishMovie" variant="primary">
                Cancel
                <b-icon icon="collection-play"></b-icon>
              </b-button>
            </div>
            <div v-else class="ms-3 mt-1">
              <b-button @click="wishMovie" variant="primary">
                Watched
                <b-icon icon="collection-play-fill"></b-icon>
              </b-button>
            </div>
            <b-form-rating v-model="renewAverage" readonly no-border size="lg" style="background-color: rgb(36, 33, 33); width: 60%; color: yellow;" class="ms-3"></b-form-rating>

          </div>
          
          <br>
          <p style="font-size: 30px"> 상영시간 : {{ moreDetail.runtime }} 분</p>
          <br>
          <p style="font-size: 30px"> 제작사 : {{ moreDetail.production_companies[0].name }}</p>
          <br>
          <div>
            <p style="font-size: 30px; white-space: pre-wrap;">줄거리: </p>
            <div>
              <p style="font-family: 'GowunDodum-Regular'; line-height: 1.5; font-size: 20px;">{{ movieData.overview }}</p>
            </div>
          </div>
        </div>

      </div>
      <br>
      <div v-if="reviewed" class="d-flex">
        <b-form-rating v-model="ogRank" variant="warning" no-border size="lg" show-value style="margin-left: 150px; background-color: rgb(36, 33, 33); width: 30%; color: white;"></b-form-rating>
        <b-form-input type="text" v-model="ogContent" @keyup.enter="updateReview(ogReviewId)" style="margin-left: 120px;"></b-form-input>
        <b-col class="ms-2">
          <b-button variant="light" size="lg" @click="updateReview(ogReviewId)">Update</b-button>
        </b-col>
        <hr>
      </div>
      <div v-else class="d-flex">
        <b-form-rating v-model="reviewRank" variant="warning" no-border size="lg" show-value style="margin-left: 150px; background-color: rgb(36, 33, 33); width: 30%; color: white;"></b-form-rating>
        <b-form-input type="text" v-model="reviewContent" @keyup.enter="createReview" style="margin-left: 120px;"></b-form-input>
        <b-col class="ms-2">
          <b-button variant="light" size="lg" @click="createReview">Review</b-button>
        </b-col>
        <hr>
      </div>
    </div>
    <div class="container mt-3">
      <b-table :items="reviews" :fields="fields" style="color: white;">
        <template #cell(user)="data">
          <b-icon v-if="data.value === username" icon="trash-fill" class="me-4" @click="deleteReview(data.item.id)"></b-icon>
          <router-link :to="{ name: 'Profile', params:{ username: data.value }}" class="text-decoration-none text-reset">{{ data.value }}</router-link>
        </template>
      </b-table>
      <br>
    </div>
    <h1>Similar Movies</h1>
    <br><br>
    <carousel :loop="true" :mouseDrag="false" :perPage="5">
      <slide v-for="movie in similarMovies" :key="movie.id">
        <div  @click="gotoDetail(movie.id)">
          <vue-flip width="500px" height="750px" active-hover transition="1.2s">
            <template v-slot:front>
              <img :src="movie.poster_path" alt="movie" style="width:500px; height:750px; object-fit: cover;">
            </template>
            <template v-slot:back  @click="goDetail(movie.id)">
              <div style="font-size:35px">
                <br>
                <div style="width:500px">{{ movie.title }}</div>
                <br>
                <div>
                  <p><b-icon icon="star-fill" variant="warning"></b-icon> {{ movie.vote_average }}</p>
                </div>
                <br>
                <p v-for="genre in movie.genres" :key="genre.id">
                  {{ genre_list[genre] }}
                </p>
                <br>
                <div>
                <p>{{ movie.release_date }}</p>
                </div>
              </div>
            </template>
          </vue-flip>
          <br><br>
        </div>
      </slide>
    </carousel>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import { Carousel, Slide } from 'vue-carousel';
import VueFlip from 'vue-flip';

export default {
  name: 'Detail',
  components: {
    Carousel,
    Slide,
    VueFlip,
  },
  data: function () {
    return {
      selectedMovie: '',
      movieData: [],
      reviews: [],
      fields: [
        {
          key: 'user',
          label: 'User',
          formatter: value => {
            return value.username
          }
        },
        'content',
        {
          key: 'rank',
          label: 'Rating',
          formatter: value => {
            let result = '★ ' + value
            return result
          }
        },
        'rank',
        {
          key:'updated_at',
          label: 'Updated_at',
          formatter: value => {
            return this.humanize(this.now,value)
          }
        }
      ],
      similarMovies: [],
      reviewContent: null,
      reviewRank: 0,
      liked: false,
      wished: false,
      videoKey: "",
      moreDetail: [],
      reviewed: false,
      ogRank: null,
      ogContent: '',
      ogReviewId: null,
      genre_list: ['액션','모험','애니메이션','코미디','범죄','다큐멘터리','드라마','가족','판타지','역사','공포','음악','미스터리','로맨스','SF','TV 영화','스릴러','전쟁','서부'],
      now: new Date()
    }
  },
  methods : {
    getReviews: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/reviews/`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.reviews = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    checkReview: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/checkreview/`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.reviewed = res.data.reviewed
          this.ogRank = res.data.serializer.rank
          this.ogContent = res.data.serializer.content
          this.ogReviewId = res.data.serializer.id
        })
        .catch(err => {
          console.log(err)
        })
    },
    getSimilarMovies: function (movie_id) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${movie_id}/similar/`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.similarMovies = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    createReview: function () {
      const content = this.reviewContent
      const rank = this.reviewRank
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/reviews/`,
        headers: this.$store.getters.config,
        data: {
          content,
          rank
        }
      })
        .then(() => {
          this.getReviews()
          this.checkReview()
        })
        .catch(() => {
          alert('이미 댓글을 작성했어요 ㅠㅠ')
        })
    },
    updateReview: function (reviewId) {
      const content = this.ogContent
      const rank = this.ogRank
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/reviews/${reviewId}/`,
        headers: this.$store.getters.config,
        data: {
          content,
          rank
        }
      })
        .then(() => {
          this.getReviews()
        })
    },
    deleteReview: function (reviewId) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/movies/reviews/${reviewId}/`,
        headers: this.$store.getters.config
      })
        .then(() => {
          this.getReviews()
          this.checkReview()
          this.reviewRank = 0
          this.reviewContent = ''
        })
        .catch(() => {
          alert('권한이 없어요')
        })
    },
    likeMovie: function () {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/likes/`,
        headers: this.$store.getters.config,
      })
        .then(() =>{
          // this.liked = res.data.liked
          this.getLikes()
        })
    },
    getLikes: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/likes/`,
        headers: this.$store.getters.config,
      })
        .then(res =>{
          this.liked = res.data.liked
        })
    },
    wishMovie: function () {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/watch/`,
        headers: this.$store.getters.config,
      })
        .then(() =>{
          // this.wished = res.data.wished
          this.getWishs()
        })
    },
    getWishs: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.selectedMovie}/watch/`,
        headers: this.$store.getters.config,
      })
        .then(res =>{
          this.wished = res.data.wished
        })
    },
    fetchVideos: function (movie_id) {
      axios({
        method: 'get',
        url: `https://api.themoviedb.org/3/movie/${movie_id}/videos?api_key=${process.env.VUE_APP_TMDB_API_KEY}&region=KR&language=ko`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.videoKey = res.data.results[0].key
        })
        .catch(err => {
          console.log(err)
        })
    },
    moreDetails: function (movie_id) {
      axios({
        method: 'get',
        url: `https://api.themoviedb.org/3/movie/${movie_id}?api_key=${process.env.VUE_APP_TMDB_API_KEY}&language=ko`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.moreDetail = res.data
          console.log(res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    gotoDetail: function (moviePk) {
      this.$router.push({
        name: 'Detail',
        params: { movieId: moviePk }
      })
      this.$router.go()
    },
    humanize: function (now, date) {
      const moment = require('moment')
      const dateData = new Date(date)
      let r = now - dateData
      if (parseInt(r) > 43200000) {
        r = moment(dateData).format('YY.MM.DD\u00A0\u00A0HH:MM')
      } else if (parseInt(r) >= 3600000) {
        r = parseInt(parseInt(r) / 3600000).toString() + '시간 전'
      } else if (parseInt(r) >= 60000) {
        r = parseInt(parseInt(r) / 60000).toString() + '분 전'
      } else {
        r = '방금 전'
      }
      return r
    },
  },
  created() {
    const moviePk = this.$route.params.movieId
    this.selectedMovie = moviePk
    
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/${this.selectedMovie}`,
      headers: this.$store.getters.config
    })
      .then(res => {
        this.movieData = res.data
        return this.movieData
      })
      .then(res => {
        this.getSimilarMovies(res.id)
        this.fetchVideos(res.tmdb_id)
        this.moreDetails(res.tmdb_id)
      })
      .catch(err => {
        console.log(err)
        alert('영화 정보가 없습니다.')
      })
      
    this.getReviews()
    this.checkReview()
    this.getLikes()
    this.getWishs()
  },
  computed: {
    ...mapState([
      'username'
    ]),
    renewAverage: function () {
      let vote_sum = this.movieData.vote_average * this.movieData.vote_count
      let voted_count = this.movieData.vote_count
      for (let review in this.reviews) { 
        voted_count ++
        vote_sum += this.reviews[review].rank * 2
      }
      const renewAVG = vote_sum / voted_count / 2
      return Math.round(renewAVG*10)/10
    },
    videoURI: function () {
      return `https://www.youtube.com/embed/${this.videoKey}?controls=1&rel=0&autoplay=1&loop=1&playlist=${this.videoKey}`;
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');
@font-face {
  font-family: 'GowunDodum-Regular';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunDodum-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}
  .detaildiv {
    font-family: 'Poppins', sans-serif;
  }
</style>