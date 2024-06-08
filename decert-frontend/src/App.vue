<template>
  <div id="app">
    <component :is="layoutComponent">
      <router-view />
    </component>
  </div>
</template>

<style>
#app {
}
</style>

<script setup lang="ts">
import BasicLayout from "@/layouts/BasicLayout.vue";
import SimpleLayout from "@/layouts/SimpleLayout.vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { onMounted, computed } from "vue";
import ACCESS_ENUM from "@/access/accessEnum";

const route = useRoute();
const layoutComponent = computed(() => route.meta.layout || BasicLayout);

/**
 * 全局初始化函数，有全局单词调用的代码，都可以写在这里
 */
const doInit = () => {
  console.log("hello 欢迎来到我的项目");
};

onMounted(() => {
  doInit();
});

const router = useRouter();
const store = useStore();

// 路由守卫逻辑
router.beforeEach((to, from, next) => {
  console.log("to.meta?.access", to.meta?.access);
  console.log("store.state.user.loginUser", store.state.user.loginUser);

  if (to.meta?.access === ACCESS_ENUM.ADMIN) {
    if (store.state.user.loginUser?.userRole !== ACCESS_ENUM.ADMIN) {
      next("/noAuth");
      return;
    }
  }

  if (
    to.meta?.access &&
    store.state.user.loginUser.userRole === ACCESS_ENUM.NOT_LOGIN
  ) {
    next("/login");
    return;
  }

  next();
});
</script>
