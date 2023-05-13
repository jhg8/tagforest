<template>
  <div id="content" >
  <section class="welcome" ><div class="container" >
    
    <h1><img src="../img/logo.png"> <span>Tagforest</span></h1>

  </div></section>
  <section class="welcome" ><div class="container" >

    <login/>

  </div></section>
  </div>
  <footer-component></footer-component>
</template>

<script>

import Login from '@/components/Login.vue'
import FooterComponent from '@/components/FooterComponent.vue'

export default {
  name: 'WelcomeView',
  components: {
    Login,
    FooterComponent
  },
  mounted () {
    if(this.loggedIn) {
      this.$router.push({path: '/trees'});
    }
  }
}
</script>
