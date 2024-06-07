// src/store/user.ts
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
    async getLoginUser({ commit }) {
      try {
        const response = await fetch(api.checkUserName, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });
        console.log("getLoginUser response.status", response.status);
        const data = await response.json();
        if (data.isValid == true) {
          commit("updateUser", {
            userName: data.username,
            userRole: "user",
          });
        } else {
          console.error("Login failed.");
          commit("updateUser", {
            userName: "未登录",
            userRole: "notLogin",
          });
        }
      } catch (error) {
        console.error("Error logging in:", error);
        commit("updateUser", {
          userName: "未登录",
          userRole: "notLogin",
        });
      }
    },
  },

  mutations: {
    updateUser(state, payload) {
      state.loginUser = payload;
    },
  },
} as StoreOptions<any>;
