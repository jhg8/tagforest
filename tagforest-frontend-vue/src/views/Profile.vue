<template>
  <section class="profile" ><div class="container" >
    <h1>{{ loggedUser }}</h1>
  </div></section>

  <section class="control-buttons" ><div class="container" >

    <button @click="showAddTreePopup = true" >
    <font-awesome-icon icon="fa-solid fa-plus" /> New Tree
    </button>

  </div></section>

  <section class="tree-list" ><div class="container" >
    <ul>
      <li v-for="tree in treeList" v-bind:key="tree.name" >
          <button @click="activeTreeId = tree.id.toString(); showTreePopup = true" >
          {{ tree.name}}
        </button>
      </li>
    </ul>
  </div></section>

  <section v-if="showTreePopup" class="popup"><div class="container" >
  <tree-upsert :cancel="true" :id="activeTreeId" @tree-upsert="showTreePopup = false; reload(); $emit('treeUpsert')" @cancel="showTreePopup = false" />
  </div></section>

  <section v-if="showAddTreePopup" class="popup"><div class="container" >
  <tree-upsert :cancel="true" @tree-upsert="showAddTreePopup = false; reload(); $emit('treeUpsert')" @cancel="showAddTreePopup = false" />
  </div></section>

  <section class="profile" ><div class="container" >
    <p>
      <logout/>
    </p>
  </div></section>
</template>

<script>

import Logout from '@/components/Logout.vue'
import TreeUpsert from '@/components/TreeUpsert.vue'

export default {
  name: 'Profile',
  components: {
    Logout,
    TreeUpsert
  },
  emits: ['treeUpsert'],
  data () {
    return {
      loggedUser: 'Anonymous',
      // Data from backend
      treeList: null,
      // Select menus
      showTreePopup: false,
      showAddTreePopup: false,
      activeTreeId: null
    }
  },
  methods: {
    async getUser () {
      const data = await this.api({ method: 'get', url: `dj-rest-auth/user/` });
      this.loggedUser = data.username;
    },
    async reload () {
      // Get data from Backend
      const data = await this.api({ method: 'get', url: `trees/` });

      this.treeList = data;
    }
  },
  mounted () {
    this.getUser();
    this.$store.commit('disableTreeMenu');
    this.reload();
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    },
  },
}
</script>
