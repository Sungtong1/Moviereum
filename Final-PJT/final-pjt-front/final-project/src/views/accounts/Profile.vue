<template>
  <b-container>
    <followings />
    <b-row align-h="center">
      <b-col cols="4" class="text-center d-flex justify-content-center">
        <h1><strong>{{ profileName }}</strong></h1>
        <span v-if="profileName !== username">
          <b-button pill v-if="followings.includes(username)" class="mt-2 ms-3" @click="follow(profileName)">언팔로우</b-button>
          <b-button pill variant="danger" v-else class="mt-2 ms-3" @click="follow(profileName)">팔로우</b-button>
        </span>
      </b-col>
    </b-row>
    <hr>
    <b-row align-h="around">
      <b-col cols="3" class="text-center"><b-avatar size="8rem"></b-avatar></b-col>
      <b-col cols="3" class="text-center" align-self="center">
        <h3 v-b-toggle.sidebar-left>{{ followingCnt}}</h3>
        팔로워
        <b-sidebar id="sidebar-left" title="Sidebar" left no-header>
          <h4 style="margin-top: 50px;">Followers</h4>
          <div class="px-3 py-2" v-for="follow1 in followings" :key="follow1.id">
            <p @click="gotoProfile(follow1)">{{ follow1 }}</p>
          </div>
        </b-sidebar>
      </b-col>
      <b-col cols="3" class="text-center" align-self="center">
        <h3 v-b-toggle.sidebar-right>{{ followerCnt}}</h3>
        팔로잉
        <b-sidebar id="sidebar-right" title="Sidebar" right no-header>
          <h4 style="margin-top: 50px;">Followings</h4>
          <div class="px-3 py-2" v-for="follow2 in follower" :key="follow2.id">
            <p @click="gotoProfile(follow2)">{{ follow2 }}</p>
          </div>
        </b-sidebar>
      </b-col>
    </b-row>

    <b-card>
      <b-tabs content-class="mt-2" card align="center">
        <b-tab>
          <template #title>
            <b-icon icon="suit-heart"></b-icon> Like
          </template>
          <like-movie-list v-for="likeMovieId in likeMovies" :key="likeMovieId.id" :likeMovieId="likeMovieId"></like-movie-list>
        </b-tab>

        <b-tab>
          <template #title>
            <b-icon icon="collection-play"></b-icon> History
          </template>
          <wish-movie-list v-for="wishMovieId in wishMovies" :key="wishMovieId.id" :wishMovieId="wishMovieId"></wish-movie-list>
        </b-tab>

      </b-tabs>
    </b-card>
    <br><br>
  </b-container>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import LikeMovieList from '@/components/LikeMovieList'
import WishMovieList from '@/components/WishMovieList'

export default {
  name: 'Profile',
  components: {
    LikeMovieList,
    WishMovieList,

  },
  data: function () {
    return {
      profileName: '',
      profileId: 0,
      followers: [],
      followings: [],
      followingCnt: 0,
      followerCnt: 0,
      likeMovies: [],
      wishMovies: [],
    }
  },
  methods: {
    getProfile: function (profileName) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/${profileName}/profile/`,
        headers: this.$store.getters.config
      })
        .then(res=>{
          console.log(res)
          this.followers = res.data.serializer.followers
          this.followings = res.data.followings
          this.follower = res.data.followers
          this.followingCnt = res.data.followingCnt
          this.followerCnt = res.data.followerCnt
          this.profileId = res.data.userId
          // this.followers = res.data.followers
        })
        .catch(() =>{
          alert('땡')
        })
    },
    follow: function (profileName) {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/accounts/${profileName}/follow/`,
        headers: this.$store.getters.config
      })
        .then(()=>{
          this.getProfile(profileName)
        })
        .catch(() => {
          alert('땡')
        })
    },
    getLikeMovies: function (profileName) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/${profileName}/likemovies/`,
        headers: this.$store.getters.config
      })
        .then(res =>{
          this.likeMovies = res.data.like_movies_list
        })
    },
    getWishMovies: function (profileName) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/${profileName}/watchmovies/`,
        headers: this.$store.getters.config
      })
        .then(res => {
          console.log(res.data.wish_movies_list)
          this.wishMovies = res.data.wish_movies_list
        })
    },
    goToReco: function () {
      this.$router.push({ name: 'Recommendation' })
    },
    gotoProfile: function (profilename) {
      this.$router.push({ name: 'Profile', params:{username:profilename}})
      this.$router.go()
    }
  },
  created: function () {
    this.profileName = this.$route.params.username
    this.getProfile(this.profileName)
    this.getLikeMovies(this.profileName)
    this.getWishMovies(this.profileName)
  },
  computed: {
    ...mapState([
      'username'
    ])
  },
}
</script>

<style>


</style>