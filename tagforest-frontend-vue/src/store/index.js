import { createStore } from 'vuex'

export default createStore({
  state () {
    return {
      loggedIn: false
    }
  },
  mutations: {
    login(state) {
      state.loggedIn = true;
    },
    logout(state) {
      state.loggedIn = false;
    }
  },
  actions: {
  },
  modules: {
  }
})
