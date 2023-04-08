<template>

  <a href="#" @click.prevent="logout" >
    <font-awesome-icon icon="fa-solid fa-right-from-bracket" /> Logout
  </a>

</template>

<script>

export default {
  name: 'Logout',
  methods: {
    async logout () {
      await this.api({ method: 'post', url: `dj-rest-auth/logout/` });
      this.$store.commit('logout');
      this.$router.go(-1);
    }
  }
}
</script>
