import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      loggedIn: false,
      token: null,
    };
  },
  mutations: {
    login(state, token) {
      state.loggedIn = true;
      state.token = token;
      localStorage.setItem('loggedIn', true);
      localStorage.setItem('token', token);
    },
    logout(state) {
      state.loggedIn = false;
      state.token = null;
      localStorage.setItem('loggedIn', false);
      localStorage.setItem('token', null);
    },
    initStore(state) {
      if (localStorage.getItem('loggedIn') === 'true') {
        state.loggedIn = localStorage.getItem('loggedIn');
        state.token = localStorage.getItem('token');
      }
    },
  },
  actions: {
  },
  modules: {
  },
});
