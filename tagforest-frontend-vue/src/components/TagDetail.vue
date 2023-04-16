<template>
  <section class="control-buttons" ><div class="container" >
    <label class="edit-checkbox" >
      <input type="checkbox" v-model="editMode" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /> Edit</span>
    </label>
    <button @click.prevent="deleteTag()" >
    <font-awesome-icon icon="fa-solid fa-trash" /> Remove
    </button>
  </div></section>

  <section v-if="!editMode" class="category"><div class="container" >
    <router-link :to="'/trees/' + activeTreeId + '/graph#' + tag.category.name + ';'" >{{ tag.category.name }}</router-link>
  </div></section>
  <section v-if="!editMode" class="tag"><div class="container" >
    <h2>{{ tag.name }}</h2>
    <p>
      <span v-for="tag in tag.parent_set" :key="tag.id"><router-link :to="'/trees/' + activeTreeId + '/graph#' + tag.name" >{{ tag.name }}</router-link></span>
      <span v-for="tag in tag.extended_parent_set" :key="tag.id"><router-link class="extended-tag" :to="'/trees/' + activeTreeId + '/graph/#' + tag.name" >{{ tag.name }}</router-link></span>
    </p>
    <p><pre>{{ tag.content }}</pre></p>
  </div></section>
  <section v-if="editMode" class="tag"><div class="container" >
    <tag-upsert :tagid="this.tagid" @tag-upsert="getTag(); editMode = false" />
  </div></section>
</template>

<script>
import TagUpsert from '@/components/TagUpsert.vue'

export default {
  name: 'TagDetail',
  props: {
    tagid: String
  },
  components: {
    TagUpsert
  },
  computed: {
    activeTreeId () {
      return this.$store.state.activeTreeId;
    }
  },
  data () {
    return {
      tag: { name: '', category: {} },
      editMode: false
    }
  },
  methods: {
    async getTag () {
      const data = await this.api({ method: 'get', url: `extendedtags/${this.tagid}/` });
      this.tag = data;
    },
    async deleteTag () {
      await this.api({ method: 'delete',  url: `tags/${this.tagid}/`});
      this.$router.push({path: '/'});
    }
  },
  mounted () {
    this.getTag();
  }
}
</script>
