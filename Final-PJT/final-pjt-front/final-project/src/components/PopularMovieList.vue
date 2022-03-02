<template>
  <div>
    <h1>인기 영화</h1>
    <carousel :loop="true" :mouseDrag="false" :perPage="5">
      <slide v-for="movie in populars" :key="movie.id" style="width:550px; height:820px;">
        <img :src="movie.poster_path" alt="nowplaying movie" style="width:500px; height:750px;" @click="movieDetail(movie.id)" class="zoom mt-5">
      </slide>
    </carousel>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { Carousel, Slide } from 'vue-carousel';

export default {
  name: 'PopularMovieList',
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
    movieDetail: function(movieId) {
      this.$router.push({
        name: 'Detail',
        params: { movieId: movieId }
      })
    }
  },
  computed: {
    ...mapState([
      'populars'
    ])
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