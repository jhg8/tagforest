<template>
  <section class="control-buttons" ><div class="container" >
    <label class="edit-checkbox" >
      <input type="checkbox" v-model="selectModeCategory" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /> Category</span>
    </label>

    <button @click="showAddCategoryPopup = true" >
    <font-awesome-icon icon="fa-solid fa-plus" /> Category
    </button>

    <span v-if="selectModeCategory" ><button @click="deleteSelectedCategory" >
    <font-awesome-icon icon="fa-solid fa-trash" /> Category
    </button></span>
  </div></section>

  <section class="control-category" ><div class="container" >
    <span v-for="category in categoryList" v-bind:key="category.name" >
      <span v-if="selectModeCategory" >
        <div class="tag-checkbox" ><label>
          <input type="checkbox" v-model="selectCategoryIdMap[category.id]" :class="{ active: selectCategoryIdMap[category.id] }" />
          <span class="label" >{{ category.name }}</span>
        </label></div>
      </span>
      <span v-else >
        <router-link :to="getTagFilterUrl('', category.name)" :class="{ active: category.name == activeCategory }" >
          {{ category.name }}
        </router-link>
      </span>
    </span>
  </div></section>

  <section class="control-tag" ><div class="container" >
    <span v-for="tag in controlTagList" v-bind:key="tag.name" >
      <router-link :to="getTagFilterUrl(tag.name, '')" :class="{ active: filterTagMap[tag.name] }" >
        {{ tag.name }}
      </router-link>
    </span>
  </div></section>

  <section class="control-buttons" ><div class="container" >
    <label class="edit-checkbox" >
      <input type="checkbox" v-model="selectMode" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /> Tag</span>
    </label>

    <span v-if="selectMode" ><button @click="deleteSelected" >
    <font-awesome-icon icon="fa-solid fa-trash" /> Tag
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

  <section v-if="showAddCategoryPopup" class="popup"><div class="container" >
  <category-upsert @category-upsert="showAddCategoryPopup = false; reload(filterQuery)" @cancel="showAddCategoryPopup = false" />
  </div></section>

</template>

<script>
import TagUpsert from '@/components/TagUpsert.vue'
import CategoryUpsert from '@/components/CategoryUpsert.vue'

export default {
  name: 'Graph',
  data () {
    return {
      // Data from backend
      categoryList: null,
      controlTagList: null,
      tagList: null,
      // Select menus
      selectMode: false,
      selectTagIdMap: {},
      selectModeCategory: false,
      selectCategoryIdMap: {},
      showAddTagPopup: false,
      showAddCategoryPopup: false,
      // Tag filtering
      activeCategory: '',
      filterTagMap: {},
      filterQuery: ''
    }
  },
  components: {
    TagUpsert,
    CategoryUpsert
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    }
  },
  methods: {
    getTagFilterUrl (tag, category) {
      let activeCategory = ``;
      if(category) {
        activeCategory = category == this.activeCategory ? `` : category;
      }
      else {
        activeCategory = this.activeCategory;
      }

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

      if(filterTagList.length > 0 || activeCategory) {
        url += `#`;
        if(activeCategory) {
          url += `${activeCategory};`;
        }
        if(filterTagList.length > 0) {
          url += `${filterTagList.join('^')}`;
        }
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
      // Refresh select Category ID Map
      let newCategoryIdList = {};
      for(const category of data.category_list) {
        this.selectCategoryIdMap[category.id] = this.selectCategoryIdMap[category.id] || false;
        newCategoryIdList[category.id] = true;
      }
      for(const id in this.selectCategoryIdMap)
        if(!(newCategoryIdList[id] || false)) delete this.selectCategoryIdMap[id];

      // Rebuild filterTagMap
      this.filterTagMap = {};
      for(const tag of data.control_tag_list) {
        this.filterTagMap[tag.name] = false;
      }
      this.activeCategory = ``;
      if(this.filterQuery) {
        let regEx = /[()|]/;
        let querySupported = true;
        let filterQuerySplit = this.filterQuery.split(';', 2);
        let tagQuery = filterQuerySplit.at(0);
        if(filterQuerySplit.length > 1) {
          this.activeCategory = filterQuerySplit.at(0);
          tagQuery = filterQuerySplit.at(1);
        }
        if(tagQuery) {
          let queryTagList = tagQuery.split('^');
          for(const w of queryTagList)
            if(w.match(regEx)) {
              querySupported = false;
              break;
            }
          if(querySupported)
            for(const tag of queryTagList)
              this.filterTagMap[tag] = true;
        }
      }

      // Refresh tag list
      this.categoryList = data.category_list;
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
    },
    async deleteSelectedCategory () {
      for(const id in this.selectCategoryIdMap)
        if(this.selectCategoryIdMap[id]) {
          await this.api({ method: 'delete', url: `tagcategories/${id}/` });
          delete this.selectCategoryIdMap[id];
        }
      this.reload(this.filterQuery);
    }
  },
  mounted () {
    this.reload(this.$route.hash);
  }
}
</script>
