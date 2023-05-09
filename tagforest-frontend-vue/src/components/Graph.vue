<template>
  <section class="control-buttons" ><div class="container" >
    <button @click="showNewTagPopup = true" >
    <font-awesome-icon icon="fa-solid fa-plus" /> New Tag
    </button>

    <button @click="showExportPopup = true; getExportValue(activeTreeId)" >
    <font-awesome-icon icon="fa-solid fa-download" /> Export
    </button>

    <button @click="showImportPopup = true" >
    <font-awesome-icon icon="fa-solid fa-upload" /> Import
    </button>

    <label class="edit-checkbox" >
      <input type="checkbox" v-model="selectMode" ref="editinputcheckbox" @click="$refs.editinputcheckbox.blur()" >
      <span class="label" ><font-awesome-icon icon="fa-solid fa-pen-to-square" /> Select</span>
    </label>

    <span v-if="selectMode" ><button @click="deleteSelected" >
    <font-awesome-icon icon="fa-solid fa-trash" /> Remove
    </button></span>

    <span v-if="selectMode" ><button @click="showAddMultiTagPopup = true" >
    <font-awesome-icon icon="fa-solid fa-tag" /> Tag
    </button></span>

  </div></section>

  <section class="control-category" ><div class="container" >
    <span v-for="category in categoryList" v-bind:key="category.name" >
      <router-link :style="{ backgroundColor: '#' + category.color }"  :to="getControlURL('', category.name)" :class="{ active: category.name == activeCategory }" >
        {{ category.name }}
      </router-link>
    </span>
    <span v-for="category in hiddenCategoryList" v-bind:key="category.name" >
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
      :options="fullTagList"
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
        <div class="entry-checkbox" ><label :style="{ backgroundColor: '#' + tag.category.color }" >
          <span class="label" >{{ tag.name }}</span>
          <input type="checkbox" v-model="selectTagIdMap[tag.id]" :class="{ active: selectTagIdMap[tag.id] }" />
        </label></div>
      </span>
      <span v-else >
        <router-link :style="{ backgroundColor: '#' + tag.category.color }"  :to="'tag/' + tag.id" >{{ tag.name }}</router-link>
      </span>
    </span>
  </div></section>

  <section v-if="showNewTagPopup" class="popup"><div class="container" >
    <tag-upsert :category="activeCategory" :parent-set="activeControlTagSet" @tag-upsert="showNewTagPopup = false; reload(hash, activeTreeId)" @cancel="showNewTagPopup = false" />
  </div></section>

  <section v-if="showAddMultiTagPopup" class="popup"><div class="container" >
    <form class="textForm" @submit.prevent="addMultiTag()" action="#" >
      <div class="formGrid" >
        <label>Tags</label>
        <span class="select" >
          <VueMultiselect
            v-model="multiTagAddSet"
            track-by="name"
            label="name"
            :options="fullTagList"
            :max-height="450"
            :multiple="true"
          >
            <template slot="singleLabel" slot-scope="{ tag }">{{ tag.name }}</template>
          </VueMultiselect>
        </span>
      </div>

      <input type="submit" />
      <button @click.prevent="showAddMultiTagPopup = false" >Cancel</button>
    </form>
  </div></section>

  <section v-if="showExportPopup" class="popupExport"><div class="container" >
    <form class="textForm">
      <span class="textarea" ><textarea type="multiarea" v-model="exportValue" placeholder="Export" >
      </textarea></span>
      <button @click="showExportPopup = false" >Exit</button>
    </form>
  </div></section>

  <section v-if="showImportPopup" class="popupExport"><div class="container" >
    <form class="textForm" @submit.prevent="importData(); $emit('submit')" action="#" >
      <span class="textarea" ><textarea type="multiarea" v-model="importValue" placeholder="Import" >
      </textarea></span>
      <input type="submit" />
      <button @click="showImportPopup = false" >Cancel</button>
    </form>
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
      hiddenCategoryList: null,
      controlTagList: [],
      tagList: null,
      fullTagList: [],
      // Select menus
      selectMode: false,
      selectTagIdMap: {},
      selectCategoryIdMap: {},
      showNewTagPopup: false,
      showAddMultiTagPopup: false,
      multiTagAddSet: [],
      // Tag filtering
      activeCategory: '',
      activeControlTagSet: [],
      hash: '',
      // URL
      baseURL: '',
      // Export / Import
      importValue: '',
      exportValue: '',
      showExportPopup: false,
      showImportPopup: false,
    }
  },
  emits: ['import', 'cancel', 'submit'],
  components: {
    TagUpsert,
    CategoryUpsert,
    VueMultiselect
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    },
    activeTreeId () {
      return this.$store.state.activeTreeId;
    },
    activeTreeName () {
      return this.$store.state.activeTreeName;
    }
  },
  watch: {
    activeTreeId(newTreeId, oldTreeId) {
      this.reload(this.$route.hash, newTreeId);
    },
    activeTreeName(newTreeName, oldTreeName) {
      this.treeNameInput = newTreeName;
    },
    '$route.hash' (newHash, oldHash) {
      this.reload(newHash, this.activeTreeId);
    },
    selectMode(newSelectMode, oldSelectMode) {
      if(!newSelectMode) {
        for(const id in this.selectTagIdMap) {
          this.selectTagIdMap[id] = false;
        }
      }
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
    parseControlQuery(hash) {
      this.activeCategory = ``;
      this.activeControlTagSet = [];

      if(!hash)
        return

      const controlQuerySplit = hash.split(';', 2);
      let tagQuery = controlQuerySplit.at(0);
      if(controlQuerySplit.length > 1) {
        this.activeCategory = controlQuerySplit.at(0);
        tagQuery = controlQuerySplit.at(1);
      }

      if(tagQuery)
        this.activeControlTagSet = tagQuery.split('^').map(x => { return {name: x, category: { name: 'Default', tree: { name: this.activeTreeName} }, tree: { name: this.activeTreeName }}});

      for(const w of this.activeControlTagSet) {
        if(w.name.match(/[()|]/)) {
          this.activeControlTagSet = [];
          break;
        }
      }
    },
    async reload (hash, treeId) {
      this.baseURL = `trees/${treeId}/graph`;
      this.hash = hash;
      const controlQueryValue  = hash ? hash.slice(1)      : '';
      let url = hash ? `${this.baseURL}/?q=${controlQueryValue}` : this.baseURL;

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
      const newCategoryIdList = {};
      for(const category of data.category_list) {
        this.selectCategoryIdMap[category.id] = this.selectCategoryIdMap[category.id] || false;
        newCategoryIdList[category.id] = true;
      }
      for(const id in this.selectCategoryIdMap)
        if(!(newCategoryIdList[id] || false)) delete this.selectCategoryIdMap[id];

      this.parseControlQuery(controlQueryValue);

      // Refresh tag list
      this.categoryList = data.category_list;
      this.hiddenCategoryList = data.hidden_category_list;
      this.controlTagList = data.control_tag_list;
      this.tagList = data.tag_list;
      this.fullTagList = data.full_tag_list;
    },
    async deleteSelected () {
      for(const id in this.selectTagIdMap)
        if(this.selectTagIdMap[id]) {
          await this.api({ method: 'delete', url: `tags/${id}/` });
          delete this.selectTagIdMap[id];
        }
      this.reload(this.hash, this.activeTreeId);
    },
    async deleteSelectedCategory () {
      for(const id in this.selectCategoryIdMap)
        if(this.selectCategoryIdMap[id]) {
          await this.api({ method: 'delete', url: `tagcategories/${id}/` });
          delete this.selectCategoryIdMap[id];
        }
      this.reload(this.hash, this.activeTreeId);
    },
    multiSelectInput() {
      let url = this.buildURL(this.activeControlTagSet.map(x => x.name), this.activeCategory);
      this.$router.push({hash: url});
    },
    async addMultiTag() {
      for(const id in this.selectTagIdMap) {
        if(this.selectTagIdMap[id]) {
          let tag = {}
          for(const t of this.tagList) {
            if(id == t.id) {
              tag = t;
              break;
            }
          }
          const tagSet = [];
          const tagData = await this.api({ method: 'get', url: `tags/${id}/` });
          for(const parentTag of tagData.parent_set) {
            let addTag = true;
            for(const multiTagAddTag of this.multiTagAddSet) {
              if(multiTagAddTag.name == parentTag.name) {
                addTag = false;
                break;
              }
            }
            if(addTag)
              tagSet.push(parentTag);
          }
          for(const multiTagAddTag of this.multiTagAddSet)
            tagSet.push(multiTagAddTag);
          const data = {
            name: tag.name,
            category: { name: tag.category.name, tree: { name: this.activeTreeName } },
            parent_set: tagSet,
            tree: { name: this.activeTreeName },
          };
          await this.api({ method: 'put',  url: `tags/${id}/`, data: data});
        }
      }
      this.showAddMultiTagPopup = false;
      this.reload(this.hash, this.activeTreeId);
    },
    async importData () {
      const data = {
        import_value: this.importValue
      };
      await this.api({ method: 'post', url: `trees/${this.activeTreeId}/import/`, data: data});
      this.$emit('import');
      this.showImportPopup = false;
      this.reload(this.$route.hash, this.activeTreeId);
    },
    async getExportValue (treeId) {
      const data = await this.api({ method: 'get', url: `trees/${treeId}/export/` });
      this.exportValue = JSON.stringify(data.export_value);
    },
  },
  mounted () {
    if(this.activeTreeId != 0) {
      this.reload(this.$route.hash, this.activeTreeId);
    }
  }
}
</script>
