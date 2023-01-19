<template>
  <section class="control-buttons" ><div class="container" >
    <label class="edit-checkbox" >
      <input type="checkbox" v-model="editMode" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /></span>
    </label>
  </div></section>

  <section v-if="!editMode" class="tag"><div class="container" >
    <h2>{{ tag.name }}</h2>
    <p>
      <span v-for="tag in tag.parent_set" :key="tag.id"><router-link :to="'/?q=' + tag.name" >{{ tag.name }}</router-link></span>
    </p>
  </div></section>
  <section v-if="editMode" class="tag"><div class="container" >
    <tag-upsert :id="this.id" @tag-upsert="getTag" @submit="editMode = false" />
  </div></section>
</template>

<script>
import TagUpsert from '@/components/TagUpsert.vue'

export default {
  name: 'TagDetail',
  props: {
    id: String
  },
  components: {
    TagUpsert
  },
  data () {
    return {
      tag: { name: '' },
      editMode: false
    }
  },
  methods: {
    async getTag () {
      const data = await this.api({ method: 'get', url: `tags/${this.id}/` });
      this.tag = data;
    }
  },
  mounted () {
    this.getTag();
  }
}
</script>
