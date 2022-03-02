<template>
  <div>
    <hr>
    <div class="d-flex justify-content-center">
      <h1>세기의 명작! 죽기전에 꼭봐야해!</h1>
      <p class="h1 ms-5" @click="getRecoByRate"><b-icon icon="arrow-clockwise" variant="light"></b-icon></p>
    </div>
    <carousel :loop="true" :mouseDrag="false" :perPage="5">
      <slide v-for="movie in recoByRate" :key="movie.id" style="width:550px; height:820px;">
        <img :src="movie.poster_path" alt="recoRate" style="width:500px; height:750px;" @click="movieDetail(movie.id)" class="zoom mt-5">
      </slide>
    </carousel>
    <hr>
    <div class="d-flex justify-content-center">
      <h1>{{username}}님이 좋아할수도 있고 ~ 안 좋아할수도 있고~</h1>
      <p class="h1 ms-5" @click="getRecoByLike"><b-icon icon="arrow-clockwise" variant="light"></b-icon></p>
    </div>
    <carousel :loop="true" :mouseDrag="false" :perPage="5">
      <slide v-for="movie in recoByLike" :key="movie.id" style="width:550px; height:820px;">
        <img :src="movie.poster_path" alt="recoLike" style="width:500px; height:750px;" @click="movieDetail(movie.id)" class="zoom mt-5">
      </slide>
    </carousel>
  </div>
</template>

<script>
import axios from 'axios'
import { Carousel, Slide } from 'vue-carousel';
import { mapState } from 'vuex'

export default {
  name: 'Recommendation',
  components: {
    Carousel,
    Slide,
  },
  data: function () {
    return {
      recoByLike: [],
      recoByRate: [],
    }
  },
  methods: {
    getRecoByRate : function () {
      axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/recobyrate/`,
      headers: this.$store.getters.config
    })
      .then(res => {
        this.recoByRate = res.data
        // console.log(res)
      })
      .catch(() => {
        alert('추천 영화를 불러올 수 없습니다.')
      })
    },
    getRecoByLike : function () {
      axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/recobylike/`,
      headers: this.$store.getters.config
    })
      .then(res => {
        this.recoByLike = res.data
      })
      .catch(() => {
        alert('추천 영화를 불러올 수 없습니다.')
      })
    },
    movieDetail: function(movieId) {
      this.$router.push({
        name: 'Detail',
        params: { movieId: movieId }
      })
    }
  },
  created: function () {
    this.getRecoByRate()
    this.getRecoByLike()
  },
  computed: {
    ...mapState([
      'username'
    ])
  }  
}
</script>

<style>

</style>