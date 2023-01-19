<template>
  <suspense>
    <template #default>
        <entry-detail :id="$route.params.id" />
    </template>
    <template #fallback>
      <p>
        Loading...
      </p>
    </template>
  </suspense>
</template>

<script>
import EntryDetail from '@/components/EntryDetail.vue'

export default {
  name: 'EntryDetailView',
  components: {
    EntryDetail
  }
}
</script>
