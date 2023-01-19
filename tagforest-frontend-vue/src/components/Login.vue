<template>

  <form class="textForm" @submit.prevent="login" action="#" >

    <label>Username</label>
    <span class="text" ><input type="text" v-model="username" placeholder="Username" /></span>

    <label>Password</label>
    <span class="text" ><input type="password" v-model="password" placeholder="Password" /></span>

    <input type="submit" />
  </form>

</template>

<script>

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
      const data = await this.api({ method: 'post', url: `dj-rest-auth/login/`,
                                    data: {username: this.username,
                                           password: this.password}});
      this.$store.commit('login', data.key);
      this.$router.go(-1);
    }
  }
}
</script>
