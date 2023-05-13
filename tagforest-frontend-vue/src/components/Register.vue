<template>

  <form class="textForm" @submit.prevent="register" action="#" >

    <label>Username</label>
    <input type="text" v-model="username" placeholder="Username" />

    <label>Password</label>
    <input type="password" v-model="password1" placeholder="Password" />

    <label>Password confirmation</label>
    <input type="password" v-model="password2" placeholder="Password confirmation" />

    <button type="submit" >Register</button>

    <div class="separator">
    <div class="line" >  </div>
    <div class="text" >or</div>
    <div class="line" >  </div>
    </div>

    <a href="/" >Log in</a>
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
      console.log("Token: " + data.key);
      //this.$store.commit('login', data.key);
      this.$router.push('/');
    }
  }
}
</script>
