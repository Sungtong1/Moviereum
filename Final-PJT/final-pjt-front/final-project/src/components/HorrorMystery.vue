<template>
  <div>
    <h1>공포 · 미스터리</h1>
    <carousel :loop="true" :mouseDrag="false" :perPage="5">
      <slide v-for="movie in movies" :key="movie.id" style="width:550px; height:820px;">
        <img :src="movie.poster_path" alt="nowplaying movie" style="width:500px; height:750px;" @click="goDetail(movie.id)" class="zoom mt-5">
      </slide>
    </carousel>
  </div>
</template>

<script>
import axios from 'axios'
import { Carousel, Slide } from 'vue-carousel';
export default {
  components: {
    Carousel,
    Slide,
  },
  name:'HorrorMystery',
  data: function () {
    return {
      movies: []
    }
  },
  methods: {
    getMovies: function() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/genremovies/5/',
        headers: this.$store.getters.config
      })
        .then(res => {
          this.movies= res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    goDetail: function(movieId) {
      this.$router.push({
        name: 'Detail',
        params: { movieId: movieId }
      })
    }
  },
  created: function () {
    this.getMovies()
  }

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