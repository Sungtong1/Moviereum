<template>
    <div class="main">
      <h1>Welcome!</h1>
      <input type="text" name="username" id="username" placeholder="User Name" :style="input" v-model="credentials.username" class="mt-4">
      <br><br>
      <input type="password" name="password" id="password" placeholder="PASSW0RD" :style="input" v-model="credentials.password" @keyup.enter="login(credentials)">
      <br><br>
      <input type="button" value="Done!" class="button" id="done" :style="input" @click="login">
      <br>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      }
    }
  },
  methods: {
    ...mapActions([
      'login',
    ])
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');
  .main {
      background-color: white;
      position: absolute;
      top: 20%;
      left: 30%;
      width: 40%;
      text-align: center;
      padding: 5px;
      border-radius: 3rem;
      box-shadow: 0px 0px 10px 0px;
      padding-top: 3%;
      padding-bottom: 5%;
      font-family: 'Poppins', sans-serif;
      color: black;
  }
  h1 {
      cursor: default;
      user-select: none;
  }
  input {
      border-radius: 3rem;
      border: 1px rgb(131, 129, 129) solid;
      padding: 10px;
      text-align: center;
      outline: none;
      margin: 10px;
      width: 30%;
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
      font-weight: 400;
  }
  input:hover {
      box-shadow: 0px 0px 5px 0px;
  }
  input:active {
      box-shadow: 0px 0px 5px 0px;
  }
  #done {
      background: rgb(80, 82, 80);
      border: none;
  }
  .button {
      cursor: pointer;
      user-select: none;
      color: white;
  }
</style>