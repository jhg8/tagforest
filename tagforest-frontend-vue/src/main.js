import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import constants from '@/constants.js'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPenToSquare, faPlus, faCheck, faTrash, faXmark, faDownload, faUpload, faRightFromBracket, faHouse, faUser, faBox, faTag } from '@fortawesome/free-solid-svg-icons'

library.add(faPenToSquare, faPlus, faCheck, faTrash, faXmark, faDownload, faUpload, faRightFromBracket, faHouse, faUser, faBox, faTag)

const app = createApp(App)

app.use(store).use(router);
app.component('font-awesome-icon', FontAwesomeIcon)

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
