<template>
  <el-row id="globalHeader" class="grid-demo" align="middle" :wrap="false">
    <el-col flex="auto">
      <el-menu
        mode="horizontal"
        :default-active="$route.path"
        @select="doMenuClick"
      >
        <el-menu-item key="0" :style="{ padding: 0, marginRight: '38px' }">
          <div class="title-bar">
            <img class="logo" src="../assets/logo.svg" />
            <div class="title">密码库工具 by 王迪</div>
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
const store = useStore();

// 展示在菜单的路由数组
const visibleRoutes = computed(() => {
  return routes.filter((item, index) => {
    if (item.meta?.hideInMenu) {
      return false;
    }
    if (!checkAccess(store.state.user.loginUser, item.meta?.access as string)) {
      return false;
    }
    return true;
  });
});

setTimeout(() => {
  store.dispatch("user/getLoginUser", {
    userName: "管理员",
    userRole: ACCESS_ENUM.ADMIN,
  });
}, 3000);

const doMenuClick = (index: string) => {
  router.push(index);
};
</script>

<style scoped>
.title-bar {
  display: flex;
  align-items: center;
}

.title {
  color: #444;
  margin-left: 16px;
}

.logo {
  height: 96px;
}

/* 添加以下样式 */
:deep(.el-menu-item.is-active) {
  background-color: #e6f7ff;
}
</style>
