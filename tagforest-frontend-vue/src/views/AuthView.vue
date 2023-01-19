<template>
  <section ><div class="container" >
    <h1>Login</h1>

    <login/>

    <h1>Register</h1>

    <register/>

  </div></section>
</template>

<script>

import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'

export default {
  name: 'AuthView',
  components: {
    Login,
    Register
  }
}
</script>
