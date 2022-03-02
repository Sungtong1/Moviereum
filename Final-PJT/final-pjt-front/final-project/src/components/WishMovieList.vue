<template>
  <img :src="wishMovie.poster_path" alt="wishmovie" class="mx-1 my-2" style="width: 400px; height: 600px;" @click="gotoDetail(wishMovie.id)">
</template>

<script>
import axios from 'axios'

export default {
  name: 'WishMovieList',
  props: {
    wishMovieId: {
      type: Number
    }
  },
  data: function () {
    return {
      wishMovie: [],
    }
  },
  methods: {
    getMovie: function (wishMovie) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${wishMovie}`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.wishMovie = res.data
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
    }
  },
  created: function (){
    this.getMovie(this.wishMovieId)
  }
}
</script>

<style>

</style>