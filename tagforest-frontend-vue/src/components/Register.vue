<template>

  <form @submit.prevent="register" action="#" >
    <input type="text" v-model="username" placeholder="Username" />
    <input type="password" v-model="password1" placeholder="Password" />
    <input type="password" v-model="password2" placeholder="Password confirmation" />
    <input type="submit" />
  </form>

</template>

<script>

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
    async register () {
      const data = await this.api({ method: 'post', url: `dj-rest-auth/registration/`,                                         data: { username: this.username,
                                            password1: this.password1,
                                            password2: this.password2 }});
      this.$store.commit('login', data.key);
      this.$router.go(-1);
    }
  }
}
</script>
