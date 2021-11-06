import { createStore } from 'vuex'

export default createStore({
  state () {
    return {
      loggedIn: false,
      token: ''
    }
  },
  mutations: {
    login(state, token) {
      state.loggedIn = true;
      state.token = token;
    },
    logout(state) {
      state.loggedIn = false;
      state.token = '';
    }
  },
  actions: {
  },
  modules: {
  }
})
