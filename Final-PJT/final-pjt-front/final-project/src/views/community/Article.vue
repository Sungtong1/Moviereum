<template>
  <div class="container">
    <select v-model="status" class="mb-4" style="width:100px; height:35px;">
      <option value="5">전체</option>
      <option value="0">Daily</option>
      <option value="1">QnA</option>
      <option value="2">Recommend</option>
      <option value="3">Review</option>
    </select>
    <div>
      <b-row align-h="start">
        <b-col cols="2">
          <h2>Id</h2>
        </b-col>
        <b-col cols="2">
          <h2>User</h2>
        </b-col>
        <b-col cols="4"><h2>Title</h2></b-col>
        <b-col cols="4"><h2>Update</h2></b-col>
      </b-row>
      <hr>
      <article-item v-for="article in articles" :key="article.id" :article="article" :status="status"></article-item>
          
          <!-- <th>User</th>
          <th>Title</th>
          <th>Update</th> -->
    </div>
    <!-- <b-row>
      <b-col align-self="start"><button @click="gotoCreate">글쓰기</button></b-col>
    </b-row> -->
    <div class="d-flex">
      <b-button pill variant="light" class="ms-auto mb-3" @click="gotoCreate">글쓰기</b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import ArticleItem from '@/components/ArticleItem'

export default {
  name: 'Article',
  components: {
    ArticleItem,
  },
  data: function () {
    return {
      articles: [],
      status: "5",
    }
  },
  methods: {
    getArticles: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/community/',
        headers: this.$store.getters.config
      })
        .then(res => {
          this.articles = res.data
          console.log(res.data)
        })
        .catch(()=>{
          this.artiles = []
          alert('게시글이 없어요 생성할래?')
        })
    },
    gotoCreate: function () {
      this.$router.push({ name: 'ArticleCreate' })
    },
    humanize: function (now, date) {
      const moment = require('moment')
      const dateData = new Date(date)
      let r = now - dateData
      if (parseInt(r) > 43200000) {
        r = moment(dateData).format('YY.MM.DD\u00A0\u00A0HH:MM')
      } else if (parseInt(r) >= 3600000) {
        r = parseInt(parseInt(r) / 3600000).toString() + '시간 전'
      } else if (parseInt(r) >= 60000) {
        r = parseInt(parseInt(r) / 60000).toString() + '분 전'
      } else {
        r = '방금 전'
      }
      return r
    },
  },
  computed: {
    ...mapState([
      'username'
    ])
  },
  created: function () {
    this.getArticles()
  }
}
</script>

<style>
</style>