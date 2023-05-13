<template>
  <div id="content" >
  <section class="register" ><div class="container" >
    <h1>Register</h1>

    <register/>

  </div></section>
  </div>
  <footer-component></footer-component>
</template>

<script>

import Register from '@/components/Register.vue'

export default {
  name: 'RegisterView',
  components: {
    Register
  },
  mounted () {
    if(this.loggedIn) {
      this.$router.push({path: '/trees'});
    }
  }
}
</script>
