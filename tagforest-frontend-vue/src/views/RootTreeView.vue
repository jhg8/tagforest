<template>
  <router-view/>
</template>

<script>

export default {
  name: 'RootTreeView',
  beforeRouteUpdate(to, from) {
    if(to.params.id != from.params.id) {
      this.updateActiveTreeId(to);
    }
  },
  computed: {
    activeTreeId () {
      return this.$store.state.activeTreeId;
    }
  },
  watch: {
    activeTreeId (newId, oldId) {
      this.updateActiveTreeName(newId);
    }
  },
  methods: {
    async updateActiveTreeName (id) {
      const data = await this.api({ method: 'get', url: `trees/${id}/` });
      this.$store.commit('setActiveTreeName', data.name);
    },
    updateActiveTreeId (route) {
      if(route.params.id) {
        this.$store.commit('setActiveTreeId', route.params.id);
      } else {
        if(this.activeTreeId == 0) {
          this.$store.commit('setActiveTreeId', 1);
        }
        this.$router.push({ name: route.name, params: {...route.params, id: this.activeTreeId} });
      }
    }
  },
  mounted () {
    this.updateActiveTreeId(this.$route);
    this.$store.commit('enableTreeMenu');
  }
}
</script>
