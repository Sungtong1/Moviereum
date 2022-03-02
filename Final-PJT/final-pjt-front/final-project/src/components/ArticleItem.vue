<template>
  <b-row align-h="start" v-if="status == article.category || status == 5" class="my-2">
    <b-col cols="2">
      <h5>{{ article.id }}</h5>
    </b-col>
    <b-col cols="2"><h5><router-link class="text-decoration-none" style="color: white;" :to="{ name: 'Profile', params:{ username: article.user.username }}">{{ article.user.username }}</router-link></h5></b-col>
    <b-col cols="4" @click="gotoDetail(article.id)">
      <h5>{{ article.title }}</h5>
    </b-col>
    <b-col cols="4"><h5>{{ humanize(now,article.updated_at) }}</h5></b-col>
    <hr>
  </b-row>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ArticleItem',
  data: function () {
    return {
      now: new Date()
    }
  },
  props: {
    article: {
      type: Object
    },
    status: {
      type: String
    }
  },
  methods: {
    gotoDetail: function (articleId) {
      this.$router.push({ name: 'ArticleDetail', params: { articleId: articleId}})
    },
    humanize: function (now, date) {
      const moment = require('moment')
      const dateData = new Date(date)
      let r = now - dateData
      
      if (parseInt(r) > 259200000) {
        r = moment(dateData).format('YY.MM.DD\u00A0\u00A0HH:MM')
      } else if (parseInt(r) >= 86400000) {
        r = parseInt(parseInt(r) / 86400000).toString() + '일 전'
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
}
</script>

<style>

</style>