<template>
  <section class="control-buttons" ><div class="container" >

    <button @click="showAddCategoryPopup = true" >
    <font-awesome-icon icon="fa-solid fa-plus" /> Category
    </button>

  </div></section>

  <section class="category-list" ><div class="container" >
    <ul>
        <li v-for="category in categoryList" v-bind:key="category.name" >
            <button @click="activeCategoryId = category.id.toString(); showCategoryPopup = true" >{{ category.name}}</button>
        </li>
    </ul>
  </div></section>

  <section v-if="showCategoryPopup" class="popup"><div class="container" >
  <category-upsert :cancel="true" :id="activeCategoryId" @category-upsert="showCategoryPopup = false; reload()" @cancel="showCategoryPopup = false" />
  </div></section>

  <section v-if="showAddCategoryPopup" class="popup"><div class="container" >
  <category-upsert cancel="true" @category-upsert="showAddCategoryPopup = false; reload()" @cancel="showAddCategoryPopup = false" />
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
    }
  },
  methods: {
    async reload () {
      // Get data from Backend
      const data = await this.api({ method: 'get', url: 'tagcategories/' });

      this.categoryList = data;
    }
  },
  mounted () {
    this.reload();
  }
}
</script>
