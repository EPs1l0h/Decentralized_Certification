//src/store/user.ts
import { StoreOptions } from "vuex";
import api from "@/config/api";

export default {
  namespaced: true,
  state: () => ({
    loginUser: {
      userName: "未登录",
      userRole: "notLogin", // 添加用户角色信息
    },
  }),
  actions: {
    async getLoginUser({ commit }, loginUser) {
      commit("updateUser", loginUser);
    },
  },

  mutations: {
    updateUser(state, payload) {
      state.loginUser = payload;
    },
  },
} as StoreOptions<any>;
