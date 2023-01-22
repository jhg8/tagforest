<template>
  <form class="textForm" @submit.prevent="upsertTag(); $emit('submit')" action="#" >
    <label>Tag name</label>
    <span><input type="text" v-model="tagName" ref="tagname" placeholder="Tag name" /></span>
    <label>Parent tags</label>
    <span><input type="text" v-model="tagParentSet" placeholder="Parent tags (e.g., 'Biology, Chemistry')" /></span>
    <input type="submit" />
    <button v-if="!update" @click="$emit('cancel')" >Cancel</button>
  </form>

</template>

<script>
import utils from '@/utils.js'

export default {
  name: 'TagUpsert',
  emits: ['tagUpsert', 'cancel', 'submit'],
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
      await this.api(this.update ?
                     { method: 'put',  url: `tags/${this.id}/`, data: data} :
                     { method: 'post', url: `tags/`,            data: data});
      this.$emit('tagUpsert');
    },
    async getTag () {
      const data = await this.api({ method: 'get', url: `tags/${this.id}/` });
      this.tagName = data.name;
      this.tagParentSet = data.parent_set.map(x => x.name).join(', ');
    }
  },
  mounted () {
    this.update = typeof this.id !== 'undefined';
    if(this.update) {
      this.getTag();
    }
    this.$refs.tagname.focus();
  }
}
</script>
