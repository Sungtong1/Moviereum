import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from "@/router/index.js";
import createPersistedState from 'vuex-persistedstate'
Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [
    createPersistedState(),
  ],
  state: {
    authToken: localStorage.getItem('jwt'),
    username: null,
    populars: [],
    allMovies: [],
  },
  mutations: {
    GET_POPULARS: function (state, movies) {
      state.populars = movies
    },
    SET_TOKEN: function (state, token) {
      state.authToken = token
      localStorage.setItem("jwt", token)
    },
    REMOVE_TOKEN: function (state) {
      localStorage.removeItem("jwt");
      state.authToken = "";
    },
    SET_USERNAME: function (state, credentials) {
      state.username = credentials.username
      console.log(state.username)
    },
    GET_ALL_MOVIES: function (state, movies) {
      state.allMovies = movies
    }
  },
  actions: {
    getallmovies: function ({ commit }) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/all/',
        headers: this.getters.config
      })
        .then(res=> {
          console.log(res.data)
          commit('GET_ALL_MOVIES', res.data)
        })
    },
    getgenres: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/getgenres/',
        headers: this.getters.config
      })
        .then(
          this.dispatch("getpopulars"),
          this.dispatch("getallmovies")
        )
    },
    getpopulars: function ({ commit }) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/populars/',
        headers: this.getters.config
      })
        .then(res => {
          // console.log(res.data)
          commit("GET_POPULARS",res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    login: function ({ commit }, credentials) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: credentials,
      })
        .then(res => {
          commit("SET_TOKEN", res.data.token)
          commit("SET_USERNAME", credentials)
          // this.dispatch("getProfiles")
          router.push({ name: 'Home' })
        })
        .catch(() =>{
          alert('로그인 정보가 일치하지 않습니다.')
        })
    },
    logout: function ({ commit }) {
      commit("REMOVE_TOKEN");
      router.push({ name: "Login" });
    },
    signup: function (context, credentials) {
      axios({
        method: "post",
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: credentials,
      })
        .then(() => {
          this.dispatch("login", credentials);
        })
        .catch(() => {
          alert('비밀번호가 일치하지 않거나 이미 가입되어 있습니다.')
        })
    }
  },
  getters: {
    isLogin: function (state) {
      return state.authToken ? true: false;
    },
    config: function(state) {
      return {
        Authorization: `JWT ${state.authToken}`,
      }
    },
    myUsername: function (state) {
      return state.username
    }
  },
  modules: {
  }
})
