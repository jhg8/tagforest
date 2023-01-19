<template>
  <suspense>
    <template #default>
        <tag-detail :id="$route.params.id" />
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
