<template>
  <suspense>
    <template #default>
        <tag-detail :tagid="$route.params.tagid" :read-only="false" tree-id='-1' />
    </template>
    <template #fallback>
      <p>
        Loading...
      </p>
    </template>
  </suspense>
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
