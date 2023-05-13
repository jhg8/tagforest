<template>
  <tag-detail :tagid="$route.params.tagid" :read-only="false" tree-id='-1' />
</template>

<script>
import TagDetail from '@/components/TagDetail.vue'

export default {
  name: 'TagDetailView',
  components: {
    TagDetail
  }
}
</script>
