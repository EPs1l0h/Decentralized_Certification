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
          <el-input v-model="_username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="_password"
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
import axios from "axios";

const router = useRouter();
const store = useStore();

const loginForm = reactive({
  username: "",
  password: "",
});

const _username = ref("");
const _password = ref("");
const loginRules = reactive<FormRules>({
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
});

const loginFormRef = ref<FormInstance>();

const handleLogin = async () => {
  loginForm.username = _username.value;
  loginForm.password = _password.value;
  console.log("loginForm:", loginForm);
  console.log("loginFormRef:", loginFormRef.value);

  if (!loginFormRef.value) return;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      // 模拟登录成功
      console.log("登录成功?");
      store.dispatch("user/getLoginUser", {
        userName: "测试用户名",
        userRole: "user",
      });
      router.push("/home");
      console.log("登录成功?2");

      // 真实逻辑,与后端交互
      //   try {

      //     const response = await axios.post("http://localhost:8000/login_post", {
      //       name: loginForm.username,
      //       password: loginForm.password,
      //     });
      //     const { isValid } = response.data;
      //     if (isValid) {
      //       store.dispatch("user/getLoginUser");
      //       router.push("/home");
      //     } else {
      //       console.error("Login failed.");
      //     }
      //   } catch (error) {
      //     console.error("Error logging in:", error);
      //   }
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
