<template>
  <span class="entry-upsert">
    <h2 v-if="update" >Update entry</h2>
    <h2 v-else >Add entry</h2>

    <form @submit.prevent="upsertEntry" action="#" >
      <input v-model="entryName" type="text" placeholder="Entry name" />
      <input v-model="entryTags"
        type="text"
        placeholder="Tags (e.g., 'Personal, Software Design, Open-source')" />
      <textarea v-if="update" v-model="entryContent"
        type="multiarea"
        placeholder="Entry content, plain text" >
      </textarea>
      <input type="submit" />
    </form>

  </span>
</template>

<script>
import utils from '@/utils';

export default {
  name: 'EntryUpsert',
  emits: ['entryUpsert'],
  props: {
    id: String,
  },
  data() {
    return {
      entryName: '',
      entryTags: '',
      entryContent: '',
      update: false,
    };
  },
  methods: {
    async upsertEntry() {
      const tagSet = utils.parseStrList(this.entryTags).map(
        (x) => ({ name: x }),
      );
      this.entryTags = tagSet.map((x) => x.name).join(', ');
      const data = {
        name: this.entryName,
        tag_set: tagSet,
        content: this.entryContent,
      };
      await this.api(this.update
        ? { method: 'put', url: `entries/${this.id}/`, data }
        : { method: 'post', url: 'entries/', data });
      this.$emit('entryUpsert');
    },
    async getEntry() {
      const data = await this.api({ method: 'get', url: `entries/${this.id}/` });
      this.entryName = data.name;
      this.entryTags = data.tag_set.map((x) => x.name).join(', ');
      this.entryContent = data.content;
    },
  },
  mounted() {
    this.update = typeof this.id !== 'undefined';
    if (this.update) {
      this.getEntry();
    }
  },
};
</script>
