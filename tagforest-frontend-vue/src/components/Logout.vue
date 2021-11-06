<template>

  <a href="#" @click.prevent="logout" >Logout</a>

</template>

<script>

import axios from 'axios'
import constants from '@/constants.js'

export default {
  name: 'Logout',
  methods: {
    async logout () {
      const response = await axios.post(`${constants.BACKEND_URL}/dj-rest-auth/logout/`);
      delete axios.defaults.headers.common['Authorization'];
      this.$store.commit('logout');
      this.$router.go(-1);
    }
  }
}
</script>
