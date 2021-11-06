<template>
  <span class="profile">
    <h1>{{ loggedUser }}</h1>
  </span>

  <p>
    <logout/>
  </p>

</template>

<script>

import axios from 'axios'
import constants from '@/constants.js'
import Logout from '@/components/Logout.vue'

export default {
  name: 'Profile',
  components: {
    Logout
  },
  data () {
    return {
      loggedUser: 'Anonymous'
    }
  },
  methods: {
    async getUser () {
      const response = await axios.get(`${constants.BACKEND_URL}/dj-rest-auth/user/`);
      this.loggedUser = response.data.username;
    }
  },
  mounted () {
    this.getUser();
  },
}
</script>
