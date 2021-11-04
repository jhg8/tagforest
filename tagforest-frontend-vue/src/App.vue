<template>
  <nav>
    <router-link to="/">Tagforest</router-link> |
    <router-link v-if="!loggedIn" to="/auth">Login / register</router-link>
    <router-link v-else to="/profile">{{ loggedUser }}</router-link> |
    <router-link to="/about">About</router-link>
  </nav>
  <router-view/>
  <footer>
    Version <!--CURRENT_VERSION--> (<!--CURRENT_VERSION_DATE-->)
  </footer>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  width: 800px;
  margin: auto;
}

pre {
  white-space: pre-wrap;       /* Since CSS 2.1 */
  white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
  white-space: -pre-wrap;      /* Opera 4-6 */
  white-space: -o-pre-wrap;    /* Opera 7 */
  word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

footer {
  margin-top: 100px;
  text-align: center;
}

input, textarea {
  width: 700px;
}
textarea {
  height: 500px;
}

nav {
  padding: 30px;
  text-align: center;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #4b82ef;
    }
  }
}
form {
  input {
    display: block;
    margin-bottom: 10px;
  }
}
a {
  color: #2c3e50;
  &:hover {
    color: #4b82ef;
  }
  &.active {
    font-weight: bold;
    color: #ef674b;
  }
}

</style>

<script>

import axios from 'axios'
import constants from '@/constants.js'

export default {
  name: 'App',
  data () {
    return {
      loggedUser: 'Anonymous',
    }
  },
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    }
  },
  watch: {
    loggedIn (newLoggedIn, oldLoggedIn) {
      async function getUser (_this) {
        const response = await axios.get(constants.BACKEND_URL + '/dj-rest-auth/user/');
        _this.loggedUser = response.data.username;
      }
      if(newLoggedIn) {
        getUser(this);
      }
    }
  }
}
</script>
