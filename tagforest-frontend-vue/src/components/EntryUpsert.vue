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
    upsertEntry () {
      async function upsertEntry (_this) {
        const tagSet = _this.entryTags.split(',').map(x => x.trim().replace(/\s+/g, ' ')).filter(x => x).map(x => { return { name: x } });
        _this.entryTags = tagSet.map(x => x.name).join(', ');
        const data = {
          name: _this.entryName,
          tag_set: tagSet,
          content: _this.entryContent,
        };
        if ( _this.update ) {
          const response = await axios.put(constants.BACKEND_URL + '/entries/' + _this.id + '/', data);
        } else {
          const response = await axios.post(constants.BACKEND_URL + '/entries/', data);
        }
        _this.$emit('entryUpsert');
      }
      upsertEntry(this);
    }
  },
  mounted () {
    async function getEntry (_this) {
      const response = await axios.get(constants.BACKEND_URL + '/entries/' + _this.id + '/');
      _this.entryName = response.data.name;
      _this.entryTags = response.data.tag_set.map(x => x.name).join(', ');
      _this.entryContent = response.data.content;
    }
    this.update = typeof this.id !== 'undefined';
    if( this.update ) {
      getEntry(this);
    }
  }
}
</script>
