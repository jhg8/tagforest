<template>
  <span v-if="loggedIn" >
    <graph :id="activeTreeId" :read-only="false" />
  </span>
</template>

<script>
import Graph from '@/components/Graph.vue'

export default {
  name: 'GraphView',
  components: {
    Graph
  },
  computed: {
    activeTreeId () {
      return this.$store.state.activeTreeId;
    }
  },
  methods: {
    async demoLogin () {
      const data = await this.api({ method: 'post', url: `dj-rest-auth/login/`,
                                    data: { username: 'demo',
                                            password: 'p1dm4V7P'}});
      this.$store.commit('login', data.key);
    }
  },
  mounted () {
    if(this.$route.path == '/') {
      this.$router.push({path: '/trees/graph'});
    }
  }
}
</script>
