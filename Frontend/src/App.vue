<template>
  <div id="app">
    <BasicLayout />
  </div>
</template>

<style>
#app {
}
</style>
<script setup lang="ts">
import BasicLayout from "@/layouts/BasicLayout.vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { onMounted } from "vue";
import ACCESS_ENUM from "@/access/accessEnum";

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

router.beforeEach((to, from, next) => {
  // 如果用户对这个页面没有权限，那么久跳转到没有权限的页面
  if (to.meta?.access === ACCESS_ENUM.ADMIN) {
    if (store.state.user.loginUser?.role !== ACCESS_ENUM.ADMIN) {
      next("/noAuth");
      return;
    }
  }
  next();
});
</script>
