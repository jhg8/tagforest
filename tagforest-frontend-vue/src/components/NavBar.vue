<template>
  <nav><div class="container">
    <router-link to="/trees/graph">
      <font-awesome-icon icon="fa-solid fa-house" />
      <span class="text" > Home</span>
    </router-link>
    <router-link v-if="loggedIn" :to="'/trees/' + activeTreeId + '/category'">
      <font-awesome-icon icon="fa-solid fa-box" />
      <span class="text" > Categories</span>
    </router-link>
    <router-link v-if="loggedIn" to="/profile">
      <font-awesome-icon icon="fa-solid fa-user" />
      {{ loggedUser }}
    </router-link>
    <slot></slot>
  </div></nav>

</template>

<script>

export default {
  name: 'NavBar',
  data () {
    return {
      loggedUser: 'Anonymous'
    }
  },
  methods: {
    async updateUser () {
      if(this.loggedIn) {
        try {
          const data = await this.api({ method: 'get', url: `dj-rest-auth/user/` });
          this.loggedUser = data.username;
        } catch(e) {
          this.$store.commit('logout');
        }
      }
    },
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    },
    activeTreeId () {
      return this.$store.state.activeTreeId;
    }
  },
  watch: {
    loggedIn (newLoggedIn, oldLoggedIn) {
      this.updateUser();
    },
  },
  mounted () {
    this.updateUser();
  }
}
</script>
