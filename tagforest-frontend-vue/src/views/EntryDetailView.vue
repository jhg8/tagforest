<template>
  <span class="home">
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
  </span>
</template>

<script>
import EntryDetail from '@/components/EntryDetail.vue';

export default {
  name: 'EntryDetailView',
  components: {
    EntryDetail,
  },
};
</script>
