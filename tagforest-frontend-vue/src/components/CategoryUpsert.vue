<template>
  <form class="textForm" @submit.prevent="upsertCategory(); $emit('submit')" action="#" >
    <div class="formGrid" >
      <label>Name</label>
      <span class="text" ><input type="text" v-model="categoryName" ref="title" placeholder="Title" /></span>

      <label>Color</label>
      <span class="text" ><input type="text" v-model="categoryColor" placeholder="Color" /></span>

      <label>Show in results</label>
      <span class="text" >
        <label class="checkbox-label" >Show in results</label>
        <input type="checkbox" v-model="categoryResults" />
      </span>

      <label>Use as filter</label>
      <span class="text" >
        <label class="checkbox-label" >Use as filter</label>
        <input type="checkbox" v-model="categoryFilter" />
      </span>

    </div>

    <input type="submit" />
    <button v-if="cancel" @click.prevent="$emit('cancel')" >Cancel</button>
    <button v-if="update" @click.prevent="deleteCategory()" >Delete</button>
  </form>
</template>

<script>
import utils from '@/utils.js'
import constants from '@/constants.js'

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
      categoryResults: true,
      categoryFilter: true,
    }
  },
  methods: {
    async upsertCategory () {
      const data = {
        name: this.categoryName,
        color: this.categoryColor,
        show_in_results: this.categoryResults,
        use_as_filter: this.categoryFilter,
        tree: { name: this.activeTreeName },
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
      this.categoryResults = data.show_in_results;
      this.categoryFilter = data.use_as_filter;
    },
    async setDefaultColor () {
      const categoryList = await this.api({ method: 'get', url: `trees/${this.activeTreeId}/tag_category_list/` });
      const usedColorList = categoryList.map(x => { return x.color });
      const colorCountMap = {}
      let colorCountList = []
      for(const color of constants.DEFAULT_CATEGORY_COLOR_SET)
        colorCountMap[color] = 0;
      for(const color of usedColorList) {
        if(color in colorCountMap)
          colorCountMap[color] += 1;
        else
          colorCountMap[color] = 1;
      }
      for(const color in colorCountMap)
        colorCountList.push([colorCountMap[color], color]);
      colorCountList = colorCountList.sort();
      this.categoryColor = colorCountList.at(0).at(1);
    }
  },
  computed: {
    update() {
      return (typeof this.id !== 'undefined');
    },
    activeTreeId () {
      return this.$store.state.activeTreeId;
    },
    activeTreeName () {
      return this.$store.state.activeTreeName;
    }
  },
  mounted () {
    if(this.update) {
      this.getCategory();
    } else {
      this.setDefaultColor();
    }
    this.$refs.title.focus();
  }
}
</script>
