<template>
  <div>
    <div class="d-flex">
      <b-avatar class="ms-3"></b-avatar>
      <div class="container">
        <router-link class="text-decoration-none" style="color: white;" :to="{ name: 'Profile', params:{ username: comment.user.username }}"><strong>{{ comment.user.username }}</strong></router-link>
        <p>{{ comment.content }}</p>
        <p>{{ humanize(now,comment.updated_at) }}</p>
      </div>
      <div v-if="username === comment.user.username">
        <b-button variant="outline-light" @click="setUpdateStatus"> 수정 </b-button>
        <b-button class="mt-2" variant="outline-light" @click="deleteComment(comment.id)">삭제</b-button>
      </div>
    </div>
    <div v-if="wantToUpdate">
      <b-container fluid>
        <b-row>
          <b-col cols="11">
            <b-form-input v-model="commentUpdateContent" @keyup.enter="updateComment(comment.id)" :placeholder="comment.content"></b-form-input>
          </b-col>
          <b-col cols="1">
            <b-button @click="updateComment(comment.id)">확인</b-button>
          </b-col>
        </b-row>
      </b-container>
    </div>
    <hr>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  name: 'CommentItem',
  props: {
    comment: {
      type: Object,
    },
    article: {
      type: Object,
    }
  },
  data: function () {
    return {
      commentUpdateContent: null,
      wantToUpdate: false,
      now: new Date()
    }
  },
  methods: {
    setUpdateStatus: function () {
      this.wantToUpdate = !this.wantToUpdate
    },
    updateComment: function (commentId) {
      const content = this.commentUpdateContent
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/community/comment/${commentId}/`,
        headers: this.$store.getters.config,
        data: {
          content,
        }
      })
        .then(() => {
          this.wantToUpdate = !this.wantToUpdate
          // this.$router.go()
          this.makeChange(this.article.id)
        })
    },
    deleteComment: function (commentId) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/community/comment/${commentId}/`,
        headers: this.$store.getters.config
      })
        .then(() => {
          this.makeChange(this.article.id)
        })
        .catch(() => {
          alert('권한이 없어요')
        })
    },
    makeChange: function (articleId) {
      this.$emit('renewal-comment', articleId)
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
}
</script>

<style>

</style>