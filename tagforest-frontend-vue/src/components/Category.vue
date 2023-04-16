<template>
  <section class="control-buttons" ><div class="container" >

    <button @click="showAddCategoryPopup = true" >
    <font-awesome-icon icon="fa-solid fa-plus" /> New Category
    </button>

  </div></section>

  <section class="category-list" ><div class="container" >
    <ul>
      <li v-for="category in categoryList" v-bind:key="category.name" >
          <button :style="{ backgroundColor: '#' + category.color }" @click="activeCategoryId = category.id.toString(); showCategoryPopup = true" >
          {{ category.name}}
        </button>
      </li>
    </ul>
  </div></section>

  <section v-if="showCategoryPopup" class="popup"><div class="container" >
  <category-upsert :cancel="true" :id="activeCategoryId" @category-upsert="showCategoryPopup = false; reload(activeTreeId)" @cancel="showCategoryPopup = false" />
  </div></section>

  <section v-if="showAddCategoryPopup" class="popup"><div class="container" >
  <category-upsert :cancel="true" @category-upsert="showAddCategoryPopup = false; reload(activeTreeId)" @cancel="showAddCategoryPopup = false" />
  </div></section>

</template>

<script>
import CategoryUpsert from '@/components/CategoryUpsert.vue'

export default {
  name: 'Category',
  data () {
    return {
      // Data from backend
      categoryList: null,
      // Select menus
      showCategoryPopup: false,
      showAddCategoryPopup: false,
      activeCategoryId: null
    }
  },
  components: {
    CategoryUpsert
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    },
    activeTreeId () {
      return this.$store.state.activeTreeId;
    }
  },
  watch: {
    activeTreeId(newTreeId, oldTreeId) {
      this.reload(newTreeId);
    }
  },
  methods: {
    async reload (treeId) {
      // Get data from Backend
      const data = await this.api({ method: 'get', url: `trees/${treeId}/tag_category_list` });

      this.categoryList = data;
    }
  },
  mounted () {
    if(this.activeTreeId != 0) {
      this.reload(this.activeTreeId);
    }
  }
}
</script>
