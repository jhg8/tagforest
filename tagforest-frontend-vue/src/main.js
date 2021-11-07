import { createApp } from 'vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import store from './store';
import constants from './constants';

const app = createApp(App);

app.use(store).use(router);

app.mixin({
  computed: {
    loggedIn() {
      return this.$store.state.loggedIn;
    },
    token() {
      return this.$store.state.token;
    },
  },
  methods: {
    async api(_config) {
      const config = _config;
      config.url = `${constants.BACKEND_URL}/${config.url}`;
      if (this.loggedIn) {
        config.headers = { Authorization: `Token ${this.token}` };
      }
      const response = await axios(config);
      return response.data;
    },
  },
});

app.mount('#app');
