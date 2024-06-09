import HomeView from "@/views/HomeView.vue";
import ManageView from "@/views/ManageView.vue";
import VerifyView from "@/views/VerifyView.vue";
import BlockInfoView from "@/views/BlockInfoView.vue";
export const routes = [
    {
        path: "/",
        redirect: "/home",
    },
    {
        path: "/home",
        name: "首页",
        component: HomeView,
    },
    {
        path: "/certification",
        name: "持有者证书管理",
        component: ManageView,
        meta: {
            access: ACCESS_ENUM.USER, // 添加权限控制
        },
    },
    {
        path: "/verification",
        name: "验证者验证证书",
        component: VerifyView,
    },
    {
        path: "/blockInfo",
        name: "当前区块链信息",
        component: BlockInfoView,
    },
];
//# sourceMappingURL=routes.js.map