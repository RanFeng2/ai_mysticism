import { createStore } from 'vuex';

// 创建一个新的store实例
const store = createStore({
  state() {//状态定义
    return {
      // 从localStorage初始化user状态
      user: null,
      isAuthenticated: false,
    };
  },
  mutations: {//状态变更
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', user);
      state.isAuthenticated = !!user;
    },
    logout(state) {
      state.user = null;
      localStorage.removeItem('user');
      state.isAuthenticated = false;
    }
  },
  actions: {//动作，可以异步，也可以调用mutations
    // 异步操作来设置user
    setUser({ commit }, user) {
      commit('setUser', user);
    }
  },
  getters: {//计算属性
    // 获取当前user状态
    user: (state) => state.user,
    isAuthenticated: (state) => state.isAuthenticated
  }
});

export default store;
