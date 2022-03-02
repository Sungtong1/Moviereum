<template>
  <div class="container">
    <div>
      <label for="articleCategory">
        <h6><strong>카테고리</strong></h6>
      </label>
      <select name="articleCategory" id="articleCategory" v-model="articleCategory" class="form-control mb-2">
        <option value="0">Daily</option>
        <option value="1">QnA</option>
        <option value="2">Recommend</option>
        <option value="3">Review</option>
      </select>
    </div>
    <div>
      <label for="text"><h6><strong>제목</strong></h6></label>
      <input type="text" id="title" v-model="articleTitle" class="form-control mb-2">
    </div>
    <div>
      <label for="articleContent"><h6><strong>내용</strong></h6></label>
      <textarea name="articleContent" id="articleContent" v-model="articleContent" cols="30" rows="10" class="form-control"></textarea>
    </div>
    <br>
    <div class="d-flex">
      <b-button variant="outline-light" @click="updateArticle(originalArticle.id)" class="ms-auto">게시글 수정</b-button>
      <b-button variant="outline-light" @click="gotoBack" class="ms-2">취소</b-button>
    </div>
  </div>
  <!-- <div>
    <input type="text" v-model="articleTitle">
    <textarea 
      name="articleContent" 
      id="articleContent" 
      v-model="articleContent" 
      cols="30" rows="10" 
    ></textarea>
    <select name="articleCategory" id="articleCategory" v-model="articleCategory">
      <option value="0">Daily</option>
      <option value="1">QnA</option>
      <option value="2">Recommend</option>
      <option value="3">Review</option>
    </select>
    <button @click="updateArticle(originalArticle.id)">게시글 작성</button>
  </div> -->
</template>

<script>
import axios from 'axios'

export default {
  name: 'ArticleUpdate',
  data: function () {
    return {
      originalArticle: null,
      articleTitle: '',
      articleContent: '',
      articleCategory: 0,
    }
  },
  methods: {
    updateArticle: function (articleId) {
      const title = this.articleTitle
      const content = this.articleContent
      const category = this.articleCategory
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/community/${articleId}/`,
        headers: this.$store.getters.config,
        data: {title, content, category}
      })
        .then(() => {
          this.$router.push({ name: 'ArticleDetail', params: { articleId: articleId }})
        })
    },
    gotoBack: function() {
      this.$router.push({ name: 'Article'})
    },
  },
  created: function () {
    this.originalArticle = this.$route.params.article
    this.articleTitle = this.originalArticle.title
    this.articleContent = this.originalArticle.content
  }
}
</script>

<style>

</style>