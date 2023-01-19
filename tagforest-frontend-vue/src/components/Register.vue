<template>

  <form class="textForm" @submit.prevent="register" action="#" >

    <label>Username</label>
    <span class="text" ><input type="text" v-model="username" placeholder="Username" /></span>
    <label>Password</label>
    <span class="text" ><input type="password" v-model="password1" placeholder="Password" /></span>
    <label>Password confirmation</label>
    <span class="text" ><input type="password" v-model="password2" placeholder="Password confirmation" /></span>
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
