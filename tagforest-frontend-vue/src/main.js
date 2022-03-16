import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import constants from '@/constants.js'

const app = createApp(App)

app.use(store).use(router);

app.mixin({
  computed: {
    loggedIn () {
      return this.$store.state.loggedIn;
    },
    token () {
      return this.$store.state.token;
    }
  },
  methods: {
    async api (config) {
      config.url = `${constants.BACKEND_URL}/${config.url}`;
      if (this.loggedIn) {
        config.headers = {'Authorization': `Token ${this.token}`};
      }
      const response = await axios(config);
      return response.data;
    }
  },
});

app.mount('#app');
