<template>
  <span class="home">
    <span v-if="loggedIn" >
      <graph ref="graph" />
    </span>
    <span v-else>
      <p>Please <router-link to="/auth">login or register</router-link></p>
      <p>You can checkout a full demo on the <a href="#" @click.prevent="demoLogin" >public demo account</a></p>
    </span>
  </span>
</template>

<script>
import Graph from '@/components/Graph.vue'
import axios from 'axios'
import constants from '@/constants.js'

export default {
  name: 'GraphView',
  components: {
    Graph
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.reload(to.query.q);
    next();
  },
  methods: {
    reload (q) {
      this.$refs.graph.reload(q);
    },
    demoLogin () {
      async function login (_this) {
        const response = await axios.post(constants.BACKEND_URL + '/dj-rest-auth/login/', {
          username: 'demo',
          password: 'p1dm4V7P'
        });
        const key = response.data.key;
        axios.defaults.headers.common['Authorization'] = 'Token ' + key;
        _this.$store.commit('login');
      }
      login(this);
    }
  }
}
</script>
