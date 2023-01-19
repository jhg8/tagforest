<template>
  <section class="control-buttons" ><div class="container" >
    <label class="edit-checkbox" >
      <input type="checkbox" v-model="editMode" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /></span>
    </label>
  </div></section>

  <section v-if="!editMode" class="tag"><div class="container" >
    <h2>{{ entry.name }}</h2>
    <p>
      <span v-for="tag in entry.tag_set" :key="tag.id"><router-link :to="'/#' + tag.name" >{{ tag.name }}</router-link></span>
    </p>
    <p><pre>{{ entry.content }}</pre></p>
  </div></section>
  <section v-if="editMode" ><div class="container" >
    <entry-upsert :id="this.id" @entry-upsert="getEntry" @submit="editMode = false" />
  </div></section>
</template>

<script>
import EntryUpsert from '@/components/EntryUpsert.vue'

export default {
  name: 'EntryDetail',
  props: {
    id: String
  },
  components: {
    EntryUpsert
  },
  data () {
    return {
      entry: { name: '' },
      editMode: false
    }
  },
  methods: {
    async getEntry () {
      const data = await this.api({ method: 'get', url: `entries/${this.id}/` });
      this.entry = data;
    }
  },
  mounted () {
    this.getEntry();
  }
}
</script>
