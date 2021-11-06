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
import axios from 'axios'
import constants from '@/constants.js'
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
      const response = await axios.get(`${constants.BACKEND_URL}/entries/${this.id}/`);
      this.entry = response.data;
    }
  },
  mounted () {
    this.getEntry();
  }
}
</script>
