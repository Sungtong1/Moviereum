<template>
  <img :src=" likeMovie.poster_path " alt="likemovie" class="mx-1 my-2" style="width: 400px; height: 600px;" @click="gotoDetail(likeMovieId)">
</template>

<script>
import axios from 'axios'
export default {
  name: 'LikeMovieList',
  props: {
    likeMovieId: {
      type : Number
    }
  },
  data: function (){
    return {
      likeMovie: []
    }
  },
  methods:{
    getMovie : function (likeMovie) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${likeMovie}`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.likeMovie = res.data
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
    this.getMovie(this.likeMovieId)
  }
}
</script>

<style>

</style>