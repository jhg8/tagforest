<template>
  <section class="control-tag" ><div class="container" >
    <span v-for="tag in controlTagList" v-bind:key="tag.name" >
      <router-link :to="getTagFilterUrl(tag.name)" :class="{ active: filterTagMap[tag.name] }" >
        {{ tag.name }}
      </router-link>
    </span>
  </div></section>

  <section class="control-buttons" ><div class="container" >
    <label class="edit-checkbox" >
      <input type="checkbox" v-model="selectMode" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /></span>
    </label>

    <span v-if="selectMode" ><button @click="deleteSelected" >
    <font-awesome-icon icon="fa-solid fa-trash" />
    </button></span>

    <button @click="showAddTagPopup = true" >
    <font-awesome-icon icon="fa-solid fa-plus" /> Tag
    </button>
  </div></section>

  <section class="entry" ><div class="container" >
    <span v-for="tag in tagList" v-bind:key="tag.id" >
      <span v-if="selectMode" >
        <div class="entry-checkbox" ><label>
          <input type="checkbox" v-model="selectTagIdMap[tag.id]" :class="{ active: selectTagIdMap[tag.id] }" />
          <span class="label" >{{ tag.name }}</span>
        </label></div>
      </span>
      <span v-else >
        <router-link :to="'/tag/' + tag.id" >{{ tag.name }}</router-link>
      </span>
    </span>
  </div></section>

  <section v-if="showAddTagPopup" class="popup"><div class="container" >
  <tag-upsert @tag-upsert="showAddTagPopup = false; reload(filterQuery)" @cancel="showAddTagPopup = false" />
  </div></section>
  <section v-if="showAddTagPopup" class="popup"><div class="container" >
  <tag-upsert @tag-upsert="showAddTagPopup = false; reload(filterQuery)" @cancel="showAddTagPopup = false" />
  </div></section>

</template>

<script>
import TagUpsert from '@/components/TagUpsert.vue'

export default {
  name: 'Graph',
  data () {
    return {
      // Data from backend
      controlTagList: null,
      tagList: null,
      // Select menus
      selectMode: false,
      selectTagIdMap: {},
      showAddTagPopup: false,
      // Tag filtering
      filterTagMap: {},
      filterQuery: ''
    }
  },
  components: {
    TagUpsert
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    }
  },
  methods: {
    getTagFilterUrl (tag) {
      let url = ``;

      let filterTagList = [];
      for(const t in this.filterTagMap) {
        if(t == tag) {
          if(!this.filterTagMap[t])
            filterTagList.push(t);
        }
        else if(this.filterTagMap[t]) {
          filterTagList.push(t);
        }
      }

      if(filterTagList.length > 0) {
        url += `#${filterTagList.join('^')}`;
      }
      return url;
    },
    async reload (filterQuery) {
      this.filterQuery  = filterQuery ? filterQuery.slice(1)      : '';
      let url = filterQuery ? `graph/?q=${this.filterQuery}` : 'graph/';

      // Get data from Backend
      const data = await this.api({ method: 'get', url: url });

      // Refresh select Tag ID Map
      let newTagIdList = {};
      for(const tag of data.tag_list) {
        this.selectTagIdMap[tag.id] = this.selectTagIdMap[tag.id] || false;
        newTagIdList[tag.id] = true;
      }
      for(const id in this.selectTagIdMap)
        if(!(newTagIdList[id] || false)) delete this.selectTagIdMap[id];

      // Rebuild filterTagMap
      this.filterTagMap = {};
      for(const tag of data.control_tag_list) {
        this.filterTagMap[tag.name] = false;
      }
      if(this.filterQuery) {
        let regEx = /[()|]/;
        let querySupported = true;
        let queryTagList = this.filterQuery.split('^');
        for(const w of queryTagList)
          if(w.match(regEx)) {
            querySupported = false;
            break;
          }
        if(querySupported)
          for(const tag of queryTagList)
            this.filterTagMap[tag] = true;
      }

      // Refresh tag list
      this.controlTagList = data.control_tag_list;
      this.tagList = data.tag_list;
    },
    async deleteSelected () {
      for(const id in this.selectTagIdMap)
        if(this.selectTagIdMap[id]) {
          await this.api({ method: 'delete', url: `tags/${id}/` });
          delete this.selectTagIdMap[id];
        }
      this.reload(this.filterQuery);
    }
  },
  mounted () {
    this.reload(this.$route.hash);
  }
}
</script>
