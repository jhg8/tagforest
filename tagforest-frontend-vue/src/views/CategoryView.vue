<template>
  <span v-if="loggedIn" >
    <category/>
  </span>
</template>

<script>
import Category from '@/components/Category.vue'

export default {
  name: 'CategoryView',
  components: {
    Category
  }
}
</script>
