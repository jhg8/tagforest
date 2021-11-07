<template>
  <span class="tag-upsert">
    <h2 v-if="update" >Update tag</h2>
    <h2 v-else >Add tag</h2>

    <form @submit.prevent="upsertTag" action="#" >
      <input v-model="tagName" type="text" placeholder="Tag name" />
      <input v-model="tagParentSet"
        type="text"
        placeholder="Parent tags (e.g., 'Biology, Chemistry')" />
      <input type="submit" />
    </form>

  </span>
</template>

<script>
import utils from '@/utils';

export default {
  name: 'TagUpsert',
  emits: ['tagUpsert'],
  props: {
    id: String,
  },
  data() {
    return {
      tagName: '',
      tagParentSet: '',
      update: false,
    };
  },
  methods: {
    async upsertTag() {
      const tagSet = utils.parseStrList(this.tagParentSet).map(
        (x) => ({ name: x }),
      );
      this.tagParentSet = tagSet.map((x) => x.name).join(', ');
      const data = {
        name: this.tagName,
        parent_set: tagSet,
      };
      await this.api(this.update
        ? { method: 'put', url: `tags/${this.id}/`, data }
        : { method: 'post', url: 'tags/', data });
      this.$emit('tagUpsert');
    },
    async getTag() {
      const data = await this.api({ method: 'get', url: `tags/${this.id}/` });
      this.tagName = data.name;
      this.tagParentSet = data.parent_set.map((x) => x.name).join(', ');
    },
  },
  mounted() {
    this.update = typeof this.id !== 'undefined';
    if (this.update) {
      this.getTag();
    }
  },
};
</script>
