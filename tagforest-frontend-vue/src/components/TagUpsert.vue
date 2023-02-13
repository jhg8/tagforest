<template>
  <form class="textForm" @submit.prevent="upsertTag(); $emit('submit')" action="#" >
    <label>Name</label>
    <span class="text" ><input type="text" v-model="tagName" ref="title" placeholder="Title" /></span>

    <label>Tags</label>
    <span class="text" ><input type="text" v-model="tagParentSet" placeholder="Tags (e.g., 'Personal, Software Design, Open-source')" /></span>

    <span v-show="update" >
      <label>Content</label>
      <span class="textarea" ref="spantextarea" ><textarea type="multiarea" v-model="tagContent" ref="textarea" @focus="resize()" placeholder="Tag content, plain text" ></textarea></span>
    </span>

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
      tagContent: '',
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
        parent_set: tagSet,
        content: this.tagContent,
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
      this.tagContent = data.content;
    },
    resize() {
      this.$refs.textarea.style.height = 'auto';
      const height = this.$refs.textarea.scrollHeight - 4 + 'px';
      this.$refs.textarea.style.height = height;
      this.$refs.spantextarea.style.height = height;
    }
  },
  mounted () {
    this.update = typeof this.id !== 'undefined';
    if( this.update ) {
      this.getTag();
    }
    this.$refs.title.focus();
    this.resize();
  },
  updated () {
    this.resize();
  }
}
</script>
