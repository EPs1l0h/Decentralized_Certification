<!-- /src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">欢迎登录 DeCert</h2>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="loginForm.password"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
          <el-button @click="goToRegister">注册</el-button>
          <el-button @click="goToHome">返回首页</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { FormInstance, FormRules } from "element-plus";
import api from "@/config/api";

const router = useRouter();
const store = useStore();

const loginForm = reactive({
  username: "",
  password: "",
});

const loginRules = reactive<FormRules>({
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
});

const loginFormRef = ref<FormInstance>();

const handleLogin = async () => {
  if (!loginFormRef.value) return;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await fetch(api.login, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            account: loginForm.username,
            password: loginForm.password,
          }),
        });

        if (response.status === 200) {
          const data = await response.json();
          const response_username = await fetch(api.checkUserName, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          });

          const usernameData = await response_username.json();
          if (usernameData.isValid) {
            store.dispatch("user/getLoginUser", {
              userName: usernameData.username,
              userRole: "user",
            });
            router.push("/home");
          } else {
            console.error("Login verification failed.");
          }
        } else {
          console.error("Login failed.");
        }
      } catch (error) {
        console.error("Error logging in:", error);
      }
    }
  });
};

const goToRegister = () => {
  router.push("/register");
};
const goToHome = () => {
  router.push("/");
};
</script>

<style scoped>
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}
</style>
