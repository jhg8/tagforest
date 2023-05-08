<template>
  <form class="textForm" @submit.prevent="upsertTag(); $emit('submit')" action="#" >
    <div class="formGrid" >
		<label>Name</label>
		<span class="text" ><input type="text" v-model="tagName" ref="title" placeholder="Title" /></span>

		<label>Category</label>
		<span class="select" >
		<VueMultiselect
		  v-model="tagCategory"
                  placeholder="Select Category"
		  :options="categoryList"
		  :max-height="450"
		  :multiple="false"
		>
		</VueMultiselect>
		</span>

		<label>Tags</label>
		<span class="select" >
		<VueMultiselect
                  placeholder="Select Tags"
		  v-model="tagParentSet"
                  track-by="name"
                  label="name"
		  :options="tagList"
		  :max-height="450"
		  :multiple="true"
		>
          <template slot="singleLabel" slot-scope="{ tag }">{{ tag.name }}</template>
		</VueMultiselect>
		</span>

		<span ><label>Content</label></span>
		  <span class="textarea" ref="spantextarea" ><textarea type="multiarea" v-model="tagContent" ref="textarea" @focus="resize()" placeholder="Tag content" ></textarea></span>
    </div>

    <input type="submit" />
    <button v-if="!update" @click="$emit('cancel')" >Cancel</button>
  </form>
</template>

<script>
import utils from '@/utils.js'
import VueMultiselect from 'vue-multiselect'

export default {
  name: 'TagUpsert',
  emits: ['tagUpsert', 'cancel', 'submit'],
  props: {
    tagid: String,
    category: String,
    parentSet: Object
  },
  components: {
      VueMultiselect
  },
  computed: {
    activeTreeId () {
      return this.$store.state.activeTreeId;
    },
    activeTreeName () {
      return this.$store.state.activeTreeName;
    }
  },
  data () {
    return {
      tagName: '',
      tagParentSet: [],
      tagContent: '',
      tagCategory: null,
      categoryList: [],
      tagList: [],
      update: false
    }
  },
  methods: {
    async upsertTag () {
      const tagSet = this.tagParentSet;
      const data = {
        name: this.tagName,
        category: { name: this.tagCategory, tree: { name: this.activeTreeName } },
        parent_set: tagSet,
        content: this.tagContent,
        tree: { name: this.activeTreeName },
      };
      await this.api(this.update ?
                     { method: 'put',  url: `tags/${this.tagid}/`, data: data} :
                     { method: 'post', url: `tags/`,            data: data});
      this.$emit('tagUpsert');
    },
    async getTag () {
      const data = await this.api({ method: 'get', url: `tags/${this.tagid}/` });
      this.tagName = data.name;
      this.tagCategory = data.category.name;
      this.tagParentSet = data.parent_set;
      this.tagContent = data.content;
    },
    async getCategoryList () {
      const data = await this.api({ method: 'get', url: `trees/${this.activeTreeId}/tag_category_list/` });
	  this.categoryList = data.map(x => x.name);
    },
    async getTagList () {
      const data = await this.api({ method: 'get', url: `trees/${this.activeTreeId}/tag_list/` });
	  this.tagList = data;
    },
    resize() {
      this.$refs.textarea.style.height = 'auto';
      const height = this.$refs.textarea.scrollHeight - 4 + 'px';
      this.$refs.textarea.style.height = height;
      this.$refs.spantextarea.style.height = height;
    }
  },
  mounted () {
    if(this.category) {
      this.tagCategory = this.category;
    }
    if(this.parentSet) {
      for(const tag of this.parentSet) {
        this.tagParentSet.push(tag);
      }
    }
    this.update = typeof this.tagid !== 'undefined';
    if( this.update ) {
      this.getTag();
    }
    this.getCategoryList();
    this.getTagList();
    this.$refs.title.focus();
    this.resize();
  },
  updated () {
    this.resize();
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
