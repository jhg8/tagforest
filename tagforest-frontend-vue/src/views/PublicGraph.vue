<template>
  <div id="content" >
    <graph :id="$route.params.id" :read-only="true" :show-tree-name="true" />
  </div>
</template>

<script>

import NavBar from '@/components/NavBar.vue'
import Graph from '@/components/Graph.vue'

export default {
  name: 'PublicGraph',
  components: {
    Graph,
    NavBar
  }
}
</script>
