<template>
  <span v-if="loggedIn" >
    <graph ref="graph" />
  </span>
  <span v-else>
    <section ><div class="container" >
      <p>Please <router-link to="/auth">login or register</router-link></p>
      <p>You can checkout a full demo on the <a href="#" @click.prevent="demoLogin" >public demo account</a></p>
  </div></section>
  </span>
</template>

<script>
import Graph from '@/components/Graph.vue'

export default {
  name: 'GraphView',
  components: {
    Graph
  },
  beforeRouteUpdate(to, from, next) {
    this.reload(to.hash);
    next();
  },
  methods: {
    reload (q) {
      this.$refs.graph.reload(q, true);
    },
    async demoLogin () {
      const data = await this.api({ method: 'post', url: `dj-rest-auth/login/`,
                                    data: { username: 'demo',
                                            password: 'p1dm4V7P'}});
      this.$store.commit('login', data.key);
    }
  }
}
</script>
