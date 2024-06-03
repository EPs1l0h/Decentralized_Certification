import { RouteRecordRaw } from "vue-router";
import SymView from "../views/SymView.vue";
import AsyView from "../views/AsyView.vue";
import HashView from "../views/HashView.vue";
import SignView from "../views/SignView.vue";

export const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/Sym",
  },
  {
    path: "/Sym",
    name: "对称加解密",
    component: SymView,
  },
  {
    path: "/Asy",
    name: "非对称加解密",
    component: AsyView,
  },
  {
    path: "/Hash",
    name: "哈希算法",
    component: HashView,
  },
  {
    path: "/Sign",
    name: "数字签名",
    component: SignView,
  },
  {
    path: "/about",
    name: "关于我的",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
];
