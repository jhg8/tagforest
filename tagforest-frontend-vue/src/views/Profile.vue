<template>
  <nav-bar></nav-bar>
  <div id="content" >
  <section class="profile tree-section" ><div class="container" >
    <h1>{{ loggedUser }}</h1>
  </div></section>

  <section class="control-buttons tree-section" ><div class="container" >

    <ul class="inline-list control-buttons" >
      <li>
        <button @click="showAddTreePopup = true" >
        <font-awesome-icon icon="fa-solid fa-plus" /> New Tree
        </button>
      </li>
    </ul>

  </div></section>

  <section class="tree-list tree-section" ><div class="container" >
    <ul>
      <li v-for="tree in treeList" v-bind:key="tree.name" >
          <button @click="activeTreeId = tree.id.toString(); showTreePopup = true" >
            <div class="tree-view-name" >{{ tree.name }}</div>
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

  <section class="profile tree-section" ><div class="container" >
    <ul class="inline-list control-buttons" >
      <li>
        <logout/>
      </li>
    </ul>
  </div></section>
  </div>
  <footer-component></footer-component>
</template>

<script>

import Logout from '@/components/Logout.vue'
import TreeUpsert from '@/components/TreeUpsert.vue'
import NavBar from '@/components/NavBar.vue'
import FooterComponent from '@/components/FooterComponent.vue'

export default {
  name: 'Profile',
  components: {
    Logout,
    TreeUpsert,
    NavBar,
    FooterComponent
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
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    },
  },
  mounted () {
    if(!this.loggedIn) {
      this.$router.push({path: '/'});
    }
    this.getUser();
    this.reload();
  }
}
</script>
