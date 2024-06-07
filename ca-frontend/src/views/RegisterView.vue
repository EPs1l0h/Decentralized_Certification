<!-- /src/views/RegisterView.vue -->
<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 class="register-title">注册 DeCert</h2>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="registerForm.password"
            placeholder="请输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            type="password"
            v-model="registerForm.confirmPassword"
            placeholder="请再次输入密码"
          ></el-input>
        </el-form-item>
        <el-form-item label="签名算法" prop="algorithm">
          <el-select
            v-model="registerForm.algorithm"
            placeholder="请选择签名算法"
          >
            <el-option label="SM2" value="SM2"></el-option>
            <el-option label="RSA" value="RSA"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister">注册</el-button>
          <el-button @click="goToLogin">返回登录</el-button>
          <el-button @click="goToHome">返回首页</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { FormInstance, FormRules } from "element-plus";
import api from "@/config/api";

const router = useRouter();

const registerForm = reactive({
  username: "",
  password: "",
  confirmPassword: "",
  algorithm: "", // 添加算法字段
});

const registerRules = reactive<FormRules>({
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  confirmPassword: [
    { required: true, message: "请再次输入密码", trigger: "blur" },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error("两次输入的密码不一致"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  algorithm: [{ required: true, message: "请选择签名算法", trigger: "change" }],
});

const registerFormRef = ref<FormInstance>();

const handleRegister = async () => {
  if (!registerFormRef.value) return;
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await fetch(api.register, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: registerForm.username, // 添加用户名字段
            password: registerForm.password,
            password_confirm: registerForm.confirmPassword,
            algorithm: registerForm.algorithm, // 添加算法字段
          }),
        });
        console.log(response);
        if (response.status == 200) {
          router.push("/login");
        } else {
          console.error("Registration failed.");
        }
      } catch (error) {
        console.error("Error registering:", error);
      }
    }
  });
};

const goToLogin = () => {
  router.push("/login");
};
const goToHome = () => {
  router.push("/");
};
</script>

<style scoped>
.register-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}
</style>
