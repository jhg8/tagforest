import { createStore } from 'vuex'

export default createStore({
  state () {
    return {
      loggedIn: false,
      token: null,
      activeTreeId: '-1',
      activeTreeName: ''
    }
  },
  mutations: {
    login(state, token) {
      state.loggedIn = true;
      state.token = token;
      state.activeTreeId = '-1';
      localStorage.setItem('loggedIn', true);
      localStorage.setItem('token', token);
    },
    setActiveTreeId(state, treeId) {
      state.activeTreeId = treeId;
    },
    setActiveTreeName(state, treeName) {
      state.activeTreeName = treeName;
    },
    logout(state) {
      state.loggedIn = false;
      state.token = null;
      state.activeTreeId = '-1';
      localStorage.setItem('loggedIn', false);
      localStorage.setItem('token', null);
    },
    initStore(state) {
      if(localStorage.getItem('loggedIn') == 'true') {
        state.loggedIn = localStorage.getItem('loggedIn');
        state.token = localStorage.getItem('token');
      }
    }
  },
  actions: {
  },
  modules: {
  }
})
