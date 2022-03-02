<template>
<div>
  <div id="app">
    <div class="dark">
      <b-navbar>
        <b-navbar-brand class="dark">
          <router-link :to="{ name: 'Home' }" class="text-decoration-none text-white">
            <img src="./assets/logo2.png" alt="logo" style="height:60px" class="ms-1"> 
          </router-link>
        </b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav class="dark">
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ms-auto me-5">
              <span v-if="isLogin">
                <b-button variant="outline-light" size="sm" @click="searchStatus" class="mx-2 mb-2">
                  <b-icon icon="search"></b-icon>
                </b-button>
                <router-link :to="{ name: 'Recommendation' }" class="text-decoration-none text-reset mx-2"><font size="5">추천 영화</font></router-link> |
                <router-link :to="{ name: 'Article' }" class="text-decoration-none text-reset mx-2"><font size="5">커뮤니티</font></router-link> |
                <router-link :to="{ name: 'Profile', params:{ username: username } }" class="text-decoration-none text-reset mx-2"><font size="5">프로필</font></router-link> |
                <router-link @click.native="logout" to="#" class="text-decoration-none text-reset mx-2"><font size="5">로그아웃</font></router-link>
              </span>
              <span v-else>
                <router-link :to="{ name:'Login' } " class="text-decoration-none text-reset mx-2"><font size="5">로그인</font></router-link> |
                <router-link :to="{ name:'Signup' }" class="text-decoration-none text-reset mx-2"><font size="5">회원가입</font></router-link> 
              </span>           
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
  </div>
  <div v-if="toggleStatus">
    <search-bar :toggle-status="toggleStatus" @change-status="getChange"></search-bar>
  </div>
  <router-view @login="isLogin=true"/>
  <div class="login-cover">
    <img src="@/assets/페이지.jpg" alt="" style="width:100%; heigth:50%">
  </div>
</div>
</template>

<script>
// import axios from 'axios'
import { mapGetters, mapActions, mapState } from 'vuex'
import router from "@/router/index.js";
import SearchBar from '@/components/SearchBar'


export default ({
  name: 'App',
  data: function () {
    return {
      toggleStatus: false,
    }
  },
  components: {
    SearchBar,
  },
  created: function () {
    this.getgenres()
    if (!this.isLogin) {
      router.push({ name: 'Login' })
    }
  },

  methods: {
    ...mapActions([
      'logout',
      'getgenres',
    ]),
    searchStatus: function () {
      this.toggleStatus = !this.toggleStatus
    },
    // 수정 중
    getChange: function (changeStatus) {
      this.toggleStatus = changeStatus
    },
    
  },
  computed: {
    ...mapGetters([
      'isLogin',
      'config'
    ]),
    ...mapState([
      'username',
      'allMovies'
    ])
  }
})

</script>


<style>
div {
  background-color: rgb(36, 33, 33);
  color: rgb(240, 240, 228);
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: sticky;
  top: 0;
  z-index: 10;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
.login-cover {
  position: fixed;
  z-index: 3;
  width: 100vw;
  height: 100vh;
  background-color: rgb(36, 33, 33);
  animation: fadeout 3s;
  animation-fill-mode: forwards;
  animation-delay: 1s;
}
@keyframes fadeout {
    from {
        z-index: 3;
        opacity: 1;
    }
    to {
        z-index: -1;
        opacity: 0;
    }
}
</style>
