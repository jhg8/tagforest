<template>
  <span class="tag-upsert">
    <h2 v-if="update" >Update tag</h2>
    <h2 v-else >Add tag</h2>

    <form @submit.prevent="upsertTag" action="#" >
      <input type="text" v-model="tagName" placeholder="Tag name" />
      <input type="text" v-model="tagParentSet" placeholder="Parent tags (e.g., 'Biology, Chemistry')" />
      <input type="submit" />
    </form>

  </span>
</template>

<script>
import axios from 'axios'
import constants from '@/constants.js'
import utils from '@/utils.js'

export default {
  name: 'TagUpsert',
  emits: ['tagUpsert'],
  props: {
    id: String
  },
  data () {
    return {
      tagName: '',
      tagParentSet: '',
      update: false
    }
  },
  methods: {
    async upsertTag () {
      const tagSet = utils.parseStrList(this.tagParentSet).map(
                       x => { return { name: x } });
      this.tagParentSet = tagSet.map(x => x.name).join(', ');
      const data = {
        name: this.tagName,
        parent_set: tagSet
      };
      const response = await (this.update ?
                         axios.put(`${constants.BACKEND_URL}/tags/${this.id}/`, data) :
                         axios.post(`${constants.BACKEND_URL}/tags/`, data));
      this.$emit('tagUpsert');
    },
    async getTag () {
      const response = await axios.get(`${constants.BACKEND_URL}/tags/${this.id}/`);
      this.tagName = response.data.name;
      this.tagParentSet = response.data.parent_set.map(x => x.name).join(', ');
    }
  },
  mounted () {
    this.update = typeof this.id !== 'undefined';
    if(this.update) {
      this.getTag();
    }
  }
}
</script>
