<template>

  <form @submit.prevent="register" action="#" >
    <input type="text" v-model="username" placeholder="Username" />
    <input type="password" v-model="password1" placeholder="Password" />
    <input type="password" v-model="password2" placeholder="Password confirmation" />
    <input type="submit" />
  </form>

</template>

<script>

import axios from 'axios'
import constants from '@/constants.js'

export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password1: '',
      password2: ''
    }
  },
  methods: {
    register () {
      async function register (_this) {
        const response = await axios.post(constants.BACKEND_URL + '/dj-rest-auth/registration/', {
          username: _this.username,
          password1: _this.password1,
          password2: _this.password2
        });
        const key = response.data.key;
        axios.defaults.headers.common['Authorization'] = 'Token ' + key;
        const responseuser = await axios.get(constants.BACKEND_URL + '/dj-rest-auth/user/');
        _this.$store.commit('login');
        _this.$router.go(-1);
      }
      register(this);
    }
  }
}
</script>
