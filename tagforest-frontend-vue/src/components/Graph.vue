<template>
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

  <section class="control-category" ><div class="container" >
    <span v-for="category in categoryList" v-bind:key="category.name" >
      <router-link :style="{ backgroundColor: '#' + category.color }"  :to="getControlURL('', category.name)" :class="{ active: category.name == activeCategory }" >
        {{ category.name }}
      </router-link>
    </span>
  </div></section>


  <section class="control-tag" ><div class="container" >

    <span class="select" >
    <VueMultiselect
      v-model="activeControlTagSet"
      track-by="name"
      label="name"
      :options="controlTagList"
      :max-height="450"
      :multiple="true"
      @select="multiSelectInput"
      @remove="multiSelectInput"
    >
    <template slot="singleLabel" slot-scope="{ tag }">{{ tag }}</template>
    </VueMultiselect>
    </span>
  </div></section>
  <section class="control-tag" ><div class="container" >

    <span v-for="tag in controlTagList.slice(0, 50)" v-bind:key="tag.name" >
      <router-link :style="{ backgroundColor: '#' + tag.category.color }" :to="getControlURL(tag.name, '')" :class="{ active: isControlTagActive(tag) }" >
        {{ tag.name }}
      </router-link>
    </span>
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
        <router-link :style="{ backgroundColor: '#' + tag.category.color }"  :to="'/tag/' + tag.id" >{{ tag.name }}</router-link>
      </span>
    </span>
  </div></section>

  <section v-if="showAddTagPopup" class="popup"><div class="container" >
    <tag-upsert :category="activeCategory" :parent-set="activeControlTagSet.map(x => x.name)" @tag-upsert="showAddTagPopup = false; reload(controlQuery, true)" @cancel="showAddTagPopup = false" />
  </div></section>

  <section v-if="showAddCategoryPopup" class="popup"><div class="container" >
  <category-upsert @category-upsert="showAddCategoryPopup = false; reload(controlQuery, true)" @cancel="showAddCategoryPopup = false" />
  </div></section>

</template>

<script>
import VueMultiselect from 'vue-multiselect'
import TagUpsert from '@/components/TagUpsert.vue'
import CategoryUpsert from '@/components/CategoryUpsert.vue'

export default {
  name: 'Graph',
  data () {
    return {
      // Data from backend
      categoryList: null,
      controlTagList: [],
      tagList: null,
      tmp: [],
      // Select menus
      selectMode: false,
      selectTagIdMap: {},
      selectCategoryIdMap: {},
      showAddTagPopup: false,
      showAddCategoryPopup: false,
      // Tag filtering
      activeCategory: '',
      activeControlTagSet: [],
      multiselectControlTagSet: [],
      controlQuery: ''
    }
  },
  components: {
    TagUpsert,
    CategoryUpsert,
    VueMultiselect
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    }
  },
  methods: {
    isControlTagActive(tag) {
      for(const t of this.activeControlTagSet)
        if(t.name == tag.name)
          return true;
      return false;
    },
    buildURL(tagSet, category) {
      let url = ``;
      if(tagSet.length > 0 || category) {
        url += `#`;
        if(category)
          url += `${category};`;
        if(tagSet.length > 0)
          url += `${tagSet.join('^')}`;
      }
      return url;
    },
    getControlURL(tag, category) {
      let newActiveCategory = ``;
      if(category) {
        newActiveCategory = category == this.activeCategory ? `` : category;
      }
      else {
        newActiveCategory = this.activeCategory;
      }

      const newActiveControlTagSet = [];
      let tagActive = false;
      for(const t of this.activeControlTagSet) {
        if(t.name != tag)
          newActiveControlTagSet.push(t.name);
        else
          tagActive = true;
      }
      if(!tagActive && tag) {
        newActiveControlTagSet.push(tag);
      }

      return this.buildURL(newActiveControlTagSet, newActiveCategory);
    },
    parseControlQuery(controlQuery) {
      this.activeCategory = ``;
      this.activeControlTagSet = [];
      this.multiselectControlTagSet = [];

      if(!controlQuery)
        return

      const controlQuerySplit = controlQuery.split(';', 2);
      let tagQuery = controlQuerySplit.at(0);
      if(controlQuerySplit.length > 1) {
        this.activeCategory = controlQuerySplit.at(0);
        tagQuery = controlQuerySplit.at(1);
      }

      if(tagQuery)
        this.activeControlTagSet = tagQuery.split('^').map(x => { return {name: x}});

      for(const w of this.activeControlTagSet) {
        if(w.name.match(/[()|]/)) {
          this.activeControlTagSet = [];
          this.multiselectControlTagSet = [];
          break;
        }
      }
    },
    async reload (controlQuery, rebuild) {
      this.controlQuery = controlQuery;
      const controlQueryValue  = controlQuery ? controlQuery.slice(1)      : '';
      let url = controlQuery ? `graph/?q=${controlQueryValue}` : 'graph/';

      // Get data from Backend
      const data = await this.api({ method: 'get', url: url });

      if(rebuild) {
        // Refresh select Tag ID Map
        let newTagIdList = {};
        for(const tag of data.tag_list) {
          this.selectTagIdMap[tag.id] = this.selectTagIdMap[tag.id] || false;
          newTagIdList[tag.id] = true;
        }
        for(const id in this.selectTagIdMap)
          if(!(newTagIdList[id] || false)) delete this.selectTagIdMap[id];
        // Refresh select Category ID Map
        const newCategoryIdList = {};
        for(const category of data.category_list) {
          this.selectCategoryIdMap[category.id] = this.selectCategoryIdMap[category.id] || false;
          newCategoryIdList[category.id] = true;
        }
        for(const id in this.selectCategoryIdMap)
          if(!(newCategoryIdList[id] || false)) delete this.selectCategoryIdMap[id];

        this.parseControlQuery(controlQueryValue);
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
      this.reload(this.controlQuery, true);
    },
    async deleteSelectedCategory () {
      for(const id in this.selectCategoryIdMap)
        if(this.selectCategoryIdMap[id]) {
          await this.api({ method: 'delete', url: `tagcategories/${id}/` });
          delete this.selectCategoryIdMap[id];
        }
      this.reload(this.controlQuery, true);
    },
    multiSelectInput() {
      console.log("watcher");
      let url = this.buildURL(this.activeControlTagSet.map(x => x.name), this.activeCategory);
      this.$router.push({hash: url});
    }
  },
  mounted () {
    this.reload(this.$route.hash, true);
  }
}
</script>
