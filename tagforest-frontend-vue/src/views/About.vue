<template>
  <nav-bar></nav-bar>
  <div id="content" >
  <section class="about"><div class="container">
    <ul>
      <li><b>REST API backend:</b> <a href="https://api.tagforest.fr">https://api.tagforest.fr</a></li>
      <li><b>Github:</b> <a href="https://github.com/jhg8/tagforest">https://github.com/jhg8/tagforest</a></li>
    </ul>
  </div></section>
  </div>
</template>

<script>

import NavBar from '@/components/NavBar.vue'

export default {
  name: 'About',
  components: {
    NavBar
  }
}
</script>
