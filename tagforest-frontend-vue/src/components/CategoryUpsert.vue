<template>
  <form class="textForm" @submit.prevent="upsertCategory(); $emit('submit')" action="#" >
    <div class="formGrid" >
      <label>Name</label>
      <span class="text" ><input type="text" v-model="categoryName" ref="title" placeholder="Title" /></span>
    </div>

    <input type="submit" />
    <button v-if="!update" @click="$emit('cancel')" >Cancel</button>
  </form>
</template>

<script>
import utils from '@/utils.js'

export default {
  name: 'CategoryUpsert',
  emits: ['categoryUpsert', 'cancel', 'submit'],
  props: {
    id: String
  },
  data () {
    return {
      categoryName: '',
      update: false
    }
  },
  methods: {
    async upsertCategory () {
      const data = {
        name: this.categoryName,
      };
      await this.api(this.update ?
                     { method: 'put',  url: `tagcategories/${this.id}/`, data: data} :
                     { method: 'post', url: `tagcategories/`,            data: data});
      this.$emit('categoryUpsert');
    },
    async getCategory () {
      const data = await this.api({ method: 'get', url: `tagcategories/${this.id}/` });
      this.categoryName = data.name;
    },
  },
  mounted () {
    this.update = typeof this.id !== 'undefined';
    if( this.update ) {
      this.getCategory();
    }
    this.$refs.title.focus();
  }
}
</script>
