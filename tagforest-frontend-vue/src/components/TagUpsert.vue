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
    upsertTag () {
      async function upsertTag (_this) {
        const tagSet = _this.tagParentSet.split(',').map(x => x.trim().replace(/\s+/g, ' ')).filter(x => x).map(x => { return { name: x } });
        _this.tagParentSet = tagSet.map(x => x.name).join(', ');
        const data = {
          name: _this.tagName,
          parent_set: tagSet
        };
        if ( _this.update ) {
          const response = await axios.put(constants.BACKEND_URL + '/tags/' + _this.id + '/', data);
        }
        else {
          const response = await axios.post(constants.BACKEND_URL + '/tags/', data);
        }
        _this.$emit('tagUpsert');
      }
      upsertTag(this);
    }
  },
  mounted () {
    async function getTag (_this) {
      const response = await axios.get(constants.BACKEND_URL + '/tags/' + _this.id + '/');
      _this.tagName = response.data.name;
      _this.tagParentSet = response.data.parent_set.map(x => x.name).join(', ');
    }
    this.update = typeof this.id !== 'undefined';
    if( this.update )
      getTag(this);
  }
}
</script>
