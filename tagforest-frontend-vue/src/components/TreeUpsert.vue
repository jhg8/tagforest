<template>
  <form class="textForm" @submit.prevent="upsertTree(); $emit('submit')" action="#" >
    <div class="formGrid" >
      <label>Name</label>
      <span class="text" ><input type="text" v-model="treeName" ref="title" placeholder="Title" /></span>
    </div>

    <input type="submit" />
    <button v-if="cancel" @click.prevent="$emit('cancel')" >Cancel</button>
    <button v-if="update" @click.prevent="deleteTree()" >Delete</button>
  </form>
</template>

<script>
import utils from '@/utils.js'
import constants from '@/constants.js'

export default {
  name: 'TreeUpsert',
  emits: ['treeUpsert', 'cancel', 'submit'],
  props: {
    id: String,
    cancel: Boolean
  },
  data () {
    return {
      treeName: '',
    }
  },
  methods: {
    async upsertTree () {
      const data = {
        name: this.treeName,
      };
      await this.api(this.update ?
                     { method: 'put',  url: `trees/${this.id}/`, data: data} :
                     { method: 'post', url: `trees/`,            data: data});
      this.$emit('treeUpsert');
    },
    async deleteTree () {
      await this.api({ method: 'delete',  url: `trees/${this.id}/`});
      this.$emit('treeUpsert');
    },
    async getTree () {
      const data = await this.api({ method: 'get', url: `trees/${this.id}/` });
      this.treeName = data.name;
    },
  },
  computed: {
    update() {
      return (typeof this.id !== 'undefined');
    },
  },
  mounted () {
    if(this.update) {
      this.getTree();
    }
    this.$refs.title.focus();
  }
}
</script>
