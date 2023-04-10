<template>
  <form class="textForm" @submit.prevent="upsertCategory(); $emit('submit')" action="#" >
    <div class="formGrid" >
      <label>Name</label>
      <span class="text" ><input type="text" v-model="categoryName" ref="title" placeholder="Title" /></span>

      <label>Color</label>
      <span class="text" ><input type="text" v-model="categoryColor" ref="color" placeholder="Color" /></span>
    </div>

    <input type="submit" />
    <button v-if="cancel" @click.prevent="$emit('cancel')" >Cancel</button>
    <button @click.prevent="deleteCategory()" >Delete</button>
  </form>
</template>

<script>
import utils from '@/utils.js'

export default {
  name: 'CategoryUpsert',
  emits: ['categoryUpsert', 'cancel', 'submit'],
  props: {
    id: String,
    cancel: Boolean
  },
  data () {
    return {
      categoryName: '',
      categoryColor: 'ffffff',
    }
  },
  methods: {
    async upsertCategory () {
      console.log("upsert");
      const data = {
        name: this.categoryName,
        color: this.categoryColor,
      };
      await this.api(this.update ?
                     { method: 'put',  url: `tagcategories/${this.id}/`, data: data} :
                     { method: 'post', url: `tagcategories/`,            data: data});
      this.$emit('categoryUpsert');
    },
    async deleteCategory () {
      await this.api({ method: 'delete',  url: `tagcategories/${this.id}/`});
      this.$emit('categoryUpsert');
    },
    async getCategory () {
      const data = await this.api({ method: 'get', url: `tagcategories/${this.id}/` });
      this.categoryName = data.name;
      this.categoryColor = data.color;
    },
  },
  computed: {
    update() {
      return (typeof this.id !== 'undefined');
    }
  },
  mounted () {
    if( this.update ) {
      this.getCategory();
    }
    this.$refs.title.focus();
  }
}
</script>
