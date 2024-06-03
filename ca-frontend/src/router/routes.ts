import { RouteRecordRaw } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import VerifyView from "@/views/VerifyView.vue";
import BlockInfoView from "@/views/BlockInfoView.vue";
import LoginView from "@/views/LoginView.vue"; // 引入登录页面组件
import RegisterView from "@/views/RegisterView.vue";
import ACCESS_ENUM from "@/access/accessEnum"; // 引入 ACCESS_ENUM
import SimpleLayout from "@/layouts/SimpleLayout.vue";
import HolderView from "@/views/HolderView.vue";

export const routes: Array<RouteRecordRaw> = [
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
    component: HolderView,
    meta: {
      access: ACCESS_ENUM.USER, // 添加权限控制
    },
  },
  {
    path: "/verification",
    name: "验证者验证证书",
    component: VerifyView,
  },
  // {
  //   path: "/blockInfo",
  //   name: "当前区块链信息",
  //   component: BlockInfoView,
  // },
  {
    path: "/login",
    name: "登录",
    component: LoginView,
    meta: {
      layout: SimpleLayout, // 指定登录页面的布局组件
      hideInMenu: true, // 隐藏该路由
    },
  },
  {
    path: "/register",
    name: "注册",
    component: RegisterView,
    meta: {
      layout: SimpleLayout, // 指定注册页面的布局组件
      hideInMenu: true, // 隐藏该路由
    },
  },
];
