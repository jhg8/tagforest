<template>
  <span v-if="loggedIn" >
    <category ref="category" />
  </span>
  <span v-else>
    <section ><div class="container" >
      <p>Please <router-link to="/auth">login or register</router-link></p>
      <p>You can checkout a full demo on the <a href="#" @click.prevent="demoLogin" >public demo account</a></p>
  </div></section>
  </span>
</template>

<script>
import Category from '@/components/Category.vue'

export default {
  name: 'CategoryView',
  components: {
    Category
  },
  beforeRouteUpdate(to, from, next) {
    this.reload();
    next();
  },
  methods: {
    reload () {
      this.$refs.category.reload();
    },
  }
}
</script>
