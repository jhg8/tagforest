<template>
  <div class="tag-detail">
    <h2>{{ tag.name }}</h2>
    <p>
      <span v-for="tag in tag.parent_set" :key="tag.id"><router-link :to="'/?q=' + tag.name" >{{ tag.name }}</router-link> | </span>
    </p>
    <tag-upsert :id="this.id" @tag-upsert="getTag" />
  </div>
</template>

<script>
import axios from 'axios'
import constants from '@/constants.js'
import TagUpsert from '@/components/TagUpsert.vue'

export default {
  name: 'TagDetail',
  props: {
    id: String
  },
  components: {
    TagUpsert
  },
  data () {
    return {
      tag: { name: '' }
    }
  },
  methods: {
    async getTag () {
      const response = await axios.get(`${constants.BACKEND_URL}/tags/${this.id}/`);
      this.tag = response.data;
    }
  },
  mounted () {
    this.getTag();
  }
}
</script>
