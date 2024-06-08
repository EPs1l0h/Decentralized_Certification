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
        async getLoginUser({ commit, state }) {
            if (state.loginUser.userName === "未登录") {
                try {
                    const response = await axios.post("http://localhost:8000/get_username", {});
                    const { isValid, username } = response.data;
                    if (isValid) {
                        commit("updateUser", { userName: username, userRole: "user" }); // 假设默认角色为user
                    }
                    else {
                        console.error("User is not logged in.");
                        commit("updateUser", { userName: "未登录", userRole: "notLogin" });
                    }
                }
                catch (error) {
                    console.error("Error fetching username:", error);
                }
            }
        },
    },
    mutations: {
        updateUser(state, payload) {
            state.loginUser = payload;
        },
    },
};
//# sourceMappingURL=user.js.map