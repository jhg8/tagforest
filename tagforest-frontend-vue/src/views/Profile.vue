<template>
  <span class="profile">
    <h1>{{ loggedUser }}</h1>
  </span>

  <p>
    <logout/>
  </p>

</template>

<script>

import Logout from '@/components/Logout.vue';

export default {
  name: 'Profile',
  components: {
    Logout,
  },
  data() {
    return {
      loggedUser: 'Anonymous',
    };
  },
  methods: {
    async getUser() {
      const data = await this.api({ method: 'get', url: 'dj-rest-auth/user/' });
      this.loggedUser = data.username;
    },
  },
  mounted() {
    this.getUser();
  },
};
</script>
