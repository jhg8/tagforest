<template>
  <div id="content" >
    <tag-detail :tagid="$route.params.id" :read-only="true" :tree-id="$route.params.treeId" />
  </div>
</template>

<script>

import NavBar from '@/components/NavBar.vue'
import TagDetail from '@/components/TagDetail.vue'

export default {
  name: 'PublicTag',
  components: {
    NavBar,
    TagDetail
  }
}
</script>
