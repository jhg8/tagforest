<template>

  <form class="textForm" @submit.prevent="login" action="#" >

    <label>Username</label>
    <input type="text" v-model="username" placeholder="Username" />

    <label>Password</label>
    <input type="password" v-model="password" placeholder="Password" />

    <button type="submit" >Log in</button>
  
    <div class="separator">
    <div class="line" >  </div>
    <div class="text" >or</div>
    <div class="line" >  </div>
    </div>

    <a href="/register" >Register</a>

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
      this.$router.push('/trees');
    }
  }
}
</script>
