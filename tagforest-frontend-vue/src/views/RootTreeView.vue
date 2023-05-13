<template>
  <nav-bar>
    <span v-if="loggedIn" class="dropdown" >
      <button @click.prevent="toggleDropdown = !toggleDropdown" ><font-awesome-icon icon="fa-solid fa-caret-down" /> {{ activeTreeName }}</button>
      <div v-if="toggleDropdown" class="dropdown-content" >
        <router-link v-for="tree in treeList" :to="'/trees/' + tree.id + '/graph'" @click="toggleDropdown = !toggleDropdown" >{{ tree.name }}</router-link>
        <button @click.prevent="showAddTreePopup = true" ><font-awesome-icon icon='fa-solid fa-plus' /> Add Tree</button>
      </div>
    </span>
  </nav-bar>

  <section v-if="showAddTreePopup" class="popup"><div class="container" >
    <tree-upsert :cancel="true" @tree-upsert="showAddTreePopup = false; toggleDropdown = false; $router.go()" @cancel="showAddTreePopup = false; toggleDropdown = false;" />
  </div></section>

  <div id="content" >
  <router-view @tree-upsert="getTrees(activeTreeId)"/>
  </div>
  <footer-component></footer-component>
</template>

<script>

import TreeUpsert from '@/components/TreeUpsert.vue'
import NavBar from '@/components/NavBar.vue'
import FooterComponent from '@/components/FooterComponent.vue'

export default {
  name: 'RootTreeView',
  data () {
    return {
      loggedUser: 'Anonymous',
      treeList: [],
      toggleDropdown: false,
      showAddTreePopup: false,
    }
  },
  components: {
    TreeUpsert,
    NavBar,
    FooterComponent
  },
  beforeRouteUpdate(to, from) {
    if(to.params.id != from.params.id) {
      this.updateActiveTreeId(to);
    }
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
    activeTreeId (newTreeId, oldTreeId) {
      this.updateActiveTreeName(newTreeId);
      this.getTrees(newTreeId);
    }
  },
  methods: {
    async updateActiveTreeName (id) {
      const data = await this.api({ method: 'get', url: `trees/${id}/` });
      this.$store.commit('setActiveTreeName', data.name);
    },
    async setDefaultTree(route) {
      const treeData = await this.api({ method: 'get', url: `trees/` });
      this.$store.commit('setActiveTreeId', treeData.at(0).id);
      this.$router.push({ name: route.name, params: {...route.params, id: this.activeTreeId} });
    },
    async updateActiveTreeId (route) {
      if(route.params.id) {
        try {
          const treeData = await this.api({ method: 'get', url: `trees/${route.params.id}/` });
          this.$store.commit('setActiveTreeId', route.params.id);
        } catch(e) {
          this.setDefaultTree(route);
        }
      } else {
        if(this.activeTreeId == '-1')
          this.setDefaultTree(route);
        else
          this.$router.push({ name: route.name, params: {...route.params, id: this.activeTreeId} });
      }
    },
    async getTrees (treeId) {
      this.treeList = await this.api({ method: 'get', url: 'trees/' });
    }
  },
  mounted () {
    if(!this.loggedIn) {
      this.$router.push({path: '/'});
    }
    this.updateActiveTreeId(this.$route);
    this.getTrees(this.activeTreeId);
  }
}
</script>
