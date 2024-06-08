<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">欢迎来到 DeCert 世界</h2>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0px"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入你的用户名"
            prefix-icon="el-icon-user"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="loginForm.password"
            placeholder="请输入你的密码"
            prefix-icon="el-icon-lock"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" @click="handleLogin"
            >登录</el-button
          >
        </el-form-item>
      </el-form>
      <div class="sign-up-link">
        还没有账号?
        <el-button type="text" @click="goToRegister">立即注册</el-button>
      </div>
    </div>
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

        if (response.ok) {
          const data = await response.json();
          store.dispatch("user/getLoginUser", {
            userName: data.username,
            userRole: "user",
          });
          router.push("/home");
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
<style>
body {
  margin: 0;
  padding: 0;
  height: 100vh;
}
</style>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  background-color: #fff;
}

.login-card {
  width: 450px;
  background-color: #fff;
  padding: 4rem;
  border-radius: 10px;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.25);
}

.login-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  color: #333;
}

.login-form {
  width: 100%;
}

.login-form .el-form-item {
  margin-bottom: 2rem;
}

.login-form .el-input {
  height: 50px;
  font-size: 1.2rem;
}

.login-form .el-input__prefix {
  left: 10px;
  font-size: 1.5rem;
  color: #999;
}

.login-button {
  width: 100%;
  height: 50px;
  font-size: 1.2rem;
  background-color: #409eff;
  border: none;
  color: #fff;
  cursor: pointer;
  transition: 0.5s;
  margin-top: 1rem;
}

.login-button:hover {
  background-color: #66b1ff;
}

.sign-up-link {
  text-align: center;
  color: #666;
  margin-top: 2rem;
}

.sign-up-link .el-button {
  color: #409eff;
}
</style>
