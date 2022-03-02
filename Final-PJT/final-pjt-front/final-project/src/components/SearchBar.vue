<template>
  <div v-if="toggleStatus" class="container text-center mb-4">
    <input id="searchinput" type="text" class="form-control" @input="onInputChange" placeholder="영화 검색">
    <carousel
      :perPage="4"
      :navigationEnabled="true"
      :paginationEnabled="false"
    >
      <slide v-for="movie in resultQuery" :key="movie.id">
        <div>
          <p>{{ movie.title }}</p>
          <img :src="movie.poster_path" alt="영화" style="width:250px; height:375px;" @click="gotoDetail(movie.id)">
        </div>
      </slide>
    </carousel>
  </div>
  
</template>

<script>
import { mapState } from 'vuex'
import { Carousel, Slide } from 'vue-carousel';

export default {
  name: 'SearchBar',
  data: function () {
    return {
      searchQuery: null,
      searchMovies: [],
      netx:'next',
    }
  },
  components: {
    Carousel,
    Slide,
  },
  props: {
    toggleStatus: Boolean
  },
  methods: {
    onInputChange: function (event) {
      this.searchQuery = event.target.value
    },
    gotoDetail: function (moviePk) {
      this.searchQuery = ''
      this.changeStatus(false)
      this.$router.push({
        name: 'Detail',
        params: { movieId: moviePk }
      })
      this.$router.go()
    },
    changeStatus: function (makeFalse) {
      this.$emit('change-status', makeFalse)
    }
  },
  computed: {
    ...mapState([
      'allMovies',
    ]),
    resultQuery(){
      if (this.searchQuery){
        return this.allMovies.filter((item)=> {
          return this.searchQuery.toLowerCase().split(' ').every(v=> item.title.toLowerCase().includes(v))
        })
      } else{
        return [];
      }
    }
  }
}
</script>

<style>
  #searchinput {
    background-color: rgb(36, 33, 33);
    color: rgb(240, 240, 228);
    font-size: 20px;
  }
  .VueCarousel-navigation-button {
    font-size: 30px;
}

</style>