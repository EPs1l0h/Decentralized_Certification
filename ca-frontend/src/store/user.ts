import { StoreOptions } from "vuex";
import axios from "axios";

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
      if (loginUser) {
        commit("updateUser", loginUser);
      } else {
        // 模拟从后端获取登录用户信息
        const mockUser = {
          userName: "张三",
          userRole: "user",
        };
        commit("updateUser", mockUser);

        // 真实逻辑,与后端交互
        // try {
        //   const response = await axios.post(
        //     "http://localhost:8000/get_username",
        //     {}
        //   );
        //   const { isValid, username } = response.data;
        //   if (isValid) {
        //     commit("updateUser", { userName: username, userRole: "user" });
        //   } else {
        //     console.error("User is not logged in.");
        //     commit("updateUser", { userName: "未登录", userRole: "notLogin" });
        //   }
        // } catch (error) {
        //   console.error("Error fetching username:", error);
        // }
      }
    },
  },

  mutations: {
    updateUser(state, payload) {
      state.loginUser = payload;
    },
  },
} as StoreOptions<any>;
