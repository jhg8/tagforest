<template>
  <div class="entry-detail">
    <h2>{{ entry.name }}</h2>
    <p>
      <span v-for="tag in entry.tag_set" :key="tag.id"><router-link :to="'/?q=' + tag.name" >{{ tag.name }}</router-link> | </span>
    </p>
    <p><pre>{{ entry.content }}</pre></p>
    <entry-upsert :id="this.id" @entry-upsert="getEntry" />
  </div>
</template>

<script>
import EntryUpsert from '@/components/EntryUpsert.vue'

export default {
  name: 'EntryDetail',
  props: {
    id: String
  },
  components: {
    EntryUpsert
  },
  data () {
    return {
      entry: { name: '' }
    }
  },
  methods: {
    async getEntry () {
      const data = await this.api({ method: 'get', url: `entries/${this.id}/` });
      this.entry = data;
    }
  },
  mounted () {
    this.getEntry();
  }
}
</script>
