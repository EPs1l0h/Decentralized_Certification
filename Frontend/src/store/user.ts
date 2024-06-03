import { StoreOptions } from "vuex";
import ACCESS_ENUM from "@/access/accessEnum";
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// export default {
//   namespaced: true,
//   state: () => ({
//     loginUser: {
//       userName: "未登录",
//     },
//   }),
//   actions: {
//     async getLoginUser({ commit, state }) {
//       const res = await new Promise((resolve) => {
//       console.log(res);
//       if (res.code === 0) {
//         commit("updateUser", res.data);
//       } else {
//         commit("updateUser", {
//           ...state.loginUser,
//           userRole: ACCESS_ENUM.NOT_LOGIN,
//         });
//       }
//     },
//   },
//   mutations: {
//     updateUser(state, payload) {
//       state.loginUser = payload;
//     },
//   },
// } as StoreOptions<any>;
