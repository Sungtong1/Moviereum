import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/accounts/Login'
import Signup from '@/views/accounts/Signup'
import Profile from '@/views/accounts/Profile'
import Home from '@/views/movies/Home'
import Detail from '@/views/movies/Detail'
import Recommendation from '@/views/movies/Recommendation'
import Article from '@/views/community/Article'
import ArticleCreate from '@/views/community/ArticleCreate'
import ArticleUpdate from '@/views/community/ArticleUpdate'
import ArticleDetail from '@/views/community/ArticleDetail'
import App from '@/App'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    // path: '/',
    name: 'App',
    component: App,
  },
  {
    path: '/accounts/login',
    // path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/:username',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/movies/home',
    // path: '/',  로그인 정보가 저장되어 있는 상태에서 다시 서버를 키면 Home이 나옴
    name: 'Home',
    component: Home,
  },
  {
    // path: '/movies/deatail',
    path: '/movies/:movieId',
    name: 'Detail',
    component: Detail,
  },
  {
    path: '/movies/recommendation',
    name: 'Recommendation',
    component: Recommendation,
  },
  {
    path: '/community/article',
    name: 'Article',
    component: Article,
  },
  {
    path: '/community/article/create',
    name: 'ArticleCreate',
    component: ArticleCreate,
  },
  {
    path: '/community/article/:article',
    name: 'ArticleUpdate',
    component: ArticleUpdate,
  },
  {
    path: '/community/article/detail/:articleId',
    name: 'ArticleDetail',
    component: ArticleDetail,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
