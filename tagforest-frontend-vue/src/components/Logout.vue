<template>

  <a href="#" @click.prevent="logout" >Logout</a>

</template>

<script>

import axios from 'axios'
import constants from '@/constants.js'

export default {
  name: 'Logout',
  methods: {
    logout () {
      async function logout (_this) {
        const response = await axios.post(constants.BACKEND_URL + '/dj-rest-auth/logout/');
        delete axios.defaults.headers.common['Authorization'];
        _this.$store.commit('logout');
        _this.$router.go(-1);
      }
      logout(this);
    }
  }
}
</script>
