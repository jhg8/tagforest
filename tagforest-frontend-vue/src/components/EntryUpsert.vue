<template>
  <span class="entry-upsert">
    <h2 v-if="update" >Update entry</h2>
    <h2 v-else >Add entry</h2>

    <form @submit.prevent="upsertEntry" action="#" >
      <input type="text" v-model="entryName" placeholder="Entry name" />
      <input type="text" v-model="entryTags" placeholder="Tags (e.g., 'Personal, Software Design, Open-source')" />
      <textarea v-if="update" type="multiarea" v-model="entryContent" placeholder="Entry content, plain text" ></textarea>
      <input type="submit" />
    </form>

  </span>
</template>

<script>
import axios from 'axios'
import constants from '@/constants.js'
import utils from '@/utils.js'

export default {
  name: 'EntryUpsert',
  emits: ['entryUpsert'],
  props: {
    id: String
  },
  data () {
    return {
      entryName: '',
      entryTags: '',
      entryContent: '',
      update: false
    }
  },
  methods: {
    async upsertEntry () {
      const tagSet = utils.parseStrList(this.entryTags).map(
                       x => { return { name: x } });
      this.entryTags = tagSet.map(x => x.name).join(', ');
      const data = {
        name: this.entryName,
        tag_set: tagSet,
        content: this.entryContent,
      };
      const response = await (this.update ?
                         axios.put(`${constants.BACKEND_URL}/entries/${this.id}/`, data) :
                         axios.post(`${constants.BACKEND_URL}/entries/`, data));
      this.$emit('entryUpsert');
    },
    async getEntry () {
      const response = await axios.get(`${constants.BACKEND_URL}/entries/${this.id}/`);
      this.entryName = response.data.name;
      this.entryTags = response.data.tag_set.map(x => x.name).join(', ');
      this.entryContent = response.data.content;
    }
  },
  mounted () {
    this.update = typeof this.id !== 'undefined';
    if( this.update ) {
      this.getEntry();
    }
  }
}
</script>
