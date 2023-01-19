<template>
  <form class="textForm" @submit.prevent="upsertEntry; $emit('submit')" action="#" >
    <label>Title</label>
    <span class="text" ><input type="text" v-model="entryName" ref="title" placeholder="Title" /></span>

    <label>Tags</label>
    <span class="text" ><input type="text" v-model="entryTags" placeholder="Tags (e.g., 'Personal, Software Design, Open-source')" /></span>

    <span v-show="update" >
      <label>Content</label>
      <span class="textarea" ref="spantextarea" ><textarea type="multiarea" v-model="entryContent" ref="textarea" @focus="resize()" placeholder="Entry content, plain text" ></textarea></span>
    </span>

    <input type="submit" />
    <button v-if="update" @click="$emit('cancel')" >Cancel</button>
  </form>
</template>

<script>
import utils from '@/utils.js'

export default {
  name: 'EntryUpsert',
  emits: ['entryUpsert', 'cancel', 'submit'],
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
      await this.api(this.update ?
                     { method: 'put',  url: `entries/${this.id}/`, data: data} :
                     { method: 'post', url: `entries/`,            data: data});
      this.$emit('entryUpsert');
    },
    async getEntry () {
      const data = await this.api({ method: 'get', url: `entries/${this.id}/`});
      this.entryName = data.name;
      this.entryTags = data.tag_set.map(x => x.name).join(', ');
      this.entryContent = data.content;
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
      this.getEntry();
    }
    this.$refs.title.focus();
    this.resize();
  },
  updated () {
    this.resize();
  }
}
</script>
