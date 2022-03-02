<template>
  <div class="container">
    <h1>{{ article.title }}</h1>
    <router-link class="text-decoration-none" style="color: white;" :to="{ name: 'Profile', params:{ username: article.user.username }}"><h5>{{ article.user.username }}</h5></router-link>
    <hr>
    <!-- p1. 여러 사람이 함께 사용하는 공간인 만큼 상대를 존중해주세요. -->
    <h6>⚠ 여러 사람이 함께 사용하는 공간인 만큼 상대방을 존중해주세요.</h6>
    <br>
    <p style="font-size: 25px; line-height:1.5; white-space: pre-wrap;">{{ article.content }}</p>
    <br>
    <div class="d-flex">
      <span v-if="username === article.user.username" class="ms-auto">
        <b-button variant="outline-light" @click="gotoUpdate(article)">게시글 수정</b-button>
        <b-button variant="outline-light" @click="deleteArticle(article.id)" class="ms-2">게시글 삭제</b-button>
        <b-button variant="outline-light" @click="gotoBack" class="ms-2">뒤로가기</b-button>
      </span>
      <span v-else class="ms-auto">
        <b-button variant="outline-light" @click="gotoBack" class="ms-2">뒤로가기</b-button>
      </span>
    </div>
    <hr>
    <h5>댓글</h5>
    <br>
    <comment-item v-for="comment in comments" :key="comment.id" :comment="comment" :article="article" @renewal-comment="getChange"></comment-item>
    <b-container fluid class="mb-5">
      <b-row>
        <b-col cols="11">
          <b-form-input v-model="commentContent" @keyup.enter="createComment(article.id)" placeholder="댓글을 남겨보세요😃"></b-form-input>
        </b-col>
        <b-col cols="1">
          <b-button variant="outline-light" @click="createComment(article.id)">생성</b-button>
        </b-col>
      </b-row>
    </b-container>
    
    <!-- <div class="d-flex">
      
    </div> -->
    <!-- <div>
      <input type="text" v-model="commentContent" @keyup.enter="createComment(article.id)">
      <button @click="createComment(article.id)">생성</button>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import CommentItem from '@/components/CommentItem'

export default {
  name: 'ArticleDetail',
  data: function () {
    return {
      articleId: null,
      article: {user: { username: ''}},
      comments: [],
      commentContent: null,
    }
  },
  components: {
    CommentItem,
  },
  methods: {
    gotoUpdate: function (article) {
      this.$router.push({ name: 'ArticleUpdate', params: { article: article }})
    },
    deleteArticle: function (articleId) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/community/${articleId}/`,
        headers: this.$store.getters.config
      })
        .then(()=>{
          // this.$router.go() // 새로고침
          this.$router.push({ name: 'Article'})
        })
        .catch(()=>{
          alert('본인 글만 지울 수 있다네')
        })
    },
    getComments: function (articleId) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/community/${articleId}/comment/`,
        headers: this.$store.getters.config
      })
        .then(res => {
          this.comments = res.data
        })
    },
    gotoBack: function() {
      this.$router.push({ name: 'Article'})
    },
    createComment: function (articleId) {
      const content = this.commentContent
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/community/${articleId}/comment/`,
        headers: this.$store.getters.config,
        data: {
          content,
        }
      })
        .then(() => {
          // this.comments.push(res.data)
          this.getComments(articleId)
          this.commentContent = ''
        })
    },
    getChange: function (articleId) {
      this.getComments(articleId)
    }
  },
  created: function () {
    this.articleId = this.$route.params.articleId
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/community/${this.articleId}/`,
      headers: this.$store.getters.config,
    })
      .then(res => {
        this.article = res.data
        return this.article
      })
      .then(res => {
        this.getComments(res.id)
      })
    // this.getComments(this.article.id)
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