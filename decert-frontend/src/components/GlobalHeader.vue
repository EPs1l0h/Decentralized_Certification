<template>
  <el-row id="globalHeader" class="grid-demo" align="middle" :wrap="false">
    <el-col :span="22">
      <el-menu
        mode="horizontal"
        :default-active="$route.path"
        @select="doMenuClick"
      >
        <el-menu-item key="0" :style="{ padding: 0, marginRight: '38px' }">
          <div class="title-bar">
            <img class="logo" src="../assets/logo.svg" />
            <div class="title">BUPTBlockTrust</div>
          </div>
        </el-menu-item>
        <el-menu-item
          v-for="route in visibleRoutes"
          :key="route.path"
          :index="route.path"
        >
          {{ route.name }}
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="2">
      <div class="user-info" v-if="!isVerifierOrIssuer">
        {{ userName }}
      </div>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { routes } from "../router/routes";
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";
import { useStore } from "vuex";
import checkAccess from "@/access/checkAccess";
import ACCESS_ENUM from "@/access/accessEnum";

const router = useRouter();
const route = useRoute();
const store = useStore();

const userName = computed(() => store.state.user.loginUser.userName);

// 展示在菜单的路由数组
const visibleRoutes = computed(() => {
  return routes.filter((item, index) => {
    if (item.meta?.hideInMenu) {
      return false;
    }
    return true;
  });
  // return routes;
});

setTimeout(() => {
  store.dispatch("user/getLoginUser");
}, 3000);

const doMenuClick = (index: string) => {
  router.push(index);
};

const handleUserInfoClick = () => {
  if (store.state.user.loginUser.userRole === ACCESS_ENUM.NOT_LOGIN) {
    router.push("/login");
  }
};

// 判断当前路由是否为验证者或颁发者界面
const isVerifierOrIssuer = computed(() => {
  const verifierPaths = ["/issue", "/verifier/otherPath"]; // 添加所有验证者界面的路径
  const issuerPaths = ["/verification", "/issuer/otherPath"]; // 添加所有颁发者界面的路径
  return verifierPaths.includes(route.path) || issuerPaths.includes(route.path);
});
</script>

<style scoped>
.title-bar {
  display: flex;
  align-items: center;
}

.title {
  color: #444;
  margin-left: 16px;
  font-size: 24px; /* 字稍微大一点点 */
  font-weight: bold; /* 字稍微粗一些 */
  font-family: "Arial", sans-serif; /* 使用好看的字体 */
}

.logo {
  height: 96px;
}

.user-info {
}

/* 添加以下样式 */
:deep(.el-menu-item.is-active) {
  background-color: #e6f7ff;
}

/* 鼠标放到logo那里的时候不要有深色显示 */
.title-bar:hover {
  background-color: transparent;
}
</style>
