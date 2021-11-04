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
    getTag () {
      async function getTag (_this) {
        const response = await axios.get(constants.BACKEND_URL + '/tags/' + _this.id + '/');
        _this.tag = response.data;
      }
      getTag(this);
    }
  },
  mounted () {
    this.getTag();
  }
}
</script>
