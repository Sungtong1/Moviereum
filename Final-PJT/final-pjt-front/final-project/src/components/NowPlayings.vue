<template>
  <div class="mt-2">
    <h1>절찬 상영중! </h1>
      <carousel :autoplay="true" :loop="true" :mouseDrag="false" :perPage="5">
        <slide v-for="movie in movies" :key="movie.id" style="width:550px; height:820px;">
          <img :src="movie.poster_path" alt="nowplaying movie" style="width:500px; height:750px;" @click="movieDetail(movie.id)" class="zoom mt-5">
        </slide>
      </carousel>
  </div>
  
</template>

<script>
import axios from 'axios'
import { Carousel, Slide } from 'vue-carousel';

export default {
  name: 'NowPlayings',
  data: function () {
    return {
      movies: [],
    }
  },
  components: {
    Carousel,
    Slide,
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getMovie: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/nowplayings/',
        headers: this.setToken()
      })
        .then(res => {
          // console.log(res.data)
          this.movies = res.data
        })
        .catch(err => {
          console.log(err)
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
    this.getMovie()
  },
}

</script>

<style>
.zoom {
  transition: transform .15s; /* Animation */
  
}
.zoom:hover {
  transform: scale(1.1); /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
}
</style>