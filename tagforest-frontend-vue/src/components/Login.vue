<template>

  <form @submit.prevent="login" action="#" >
    <input type="text" v-model="username" placeholder="Username" />
    <input type="password" v-model="password" placeholder="Password" />
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
      password: '',
    }
  },
  methods: {
    async login () {
      const response = await axios.post(`${constants.BACKEND_URL}/dj-rest-auth/login/`, {
        username: this.username,
        password: this.password,
      });
      const key = response.data.key;
      axios.defaults.headers.common['Authorization'] = `Token ${key}`;
      this.$store.commit('login');
      this.$router.go(-1);
    }
  }
}
</script>
