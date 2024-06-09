根据 Element Plus 的 Select 组件 API 文档,我们需要对 CSS 进行以下修改: ```css
.register-select.el-select { height: 50px; } .register-select.el-select
.el-input__inner { height: 50px; } ``` 这里是修改后的完整代码:

<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">注册 DeCert</h2>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="0px"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="registerForm.password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
          ></el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input
            type="password"
            v-model="registerForm.confirmPassword"
            placeholder="请再次输入密码"
            prefix-icon="el-icon-lock"
          ></el-input>
        </el-form-item>
        <el-form-item prop="algorithm">
          <el-select
            v-model="registerForm.algorithm"
            placeholder="请选择签名算法"
            class="register-select"
            prefix-icon="el-icon-s-grid"
          >
            <el-option label="SM2" value="SM2"></el-option>
            <el-option label="RSA" value="RSA"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            class="register-button"
            @click="handleRegister"
            >注册</el-button
          >
        </el-form-item>
      </el-form>
      <div class="login-link">
        已有账号?
        <el-button type="text" @click="goToLogin">立即登录</el-button>
      </div>
      <div class="home-link">
        <el-button type="text" @click="goToHome">返回首页</el-button>
      </div>
    </div>
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
  algorithm: "",
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
            username: registerForm.username,
            password: registerForm.password,
            password_confirm: registerForm.confirmPassword,
            algorithm: registerForm.algorithm,
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
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  background-color: #fff;
}

.register-card {
  width: 450px;
  background-color: #fff;
  padding: 4rem;
  border-radius: 10px;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.25);
}

.register-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  color: #333;
}

.register-form {
  width: 100%;
}

.register-form .el-form-item {
  margin-bottom: 2rem;
}

.register-form .el-input,
.register-form .el-select {
  height: 50px;
  font-size: 1.2rem;
}

.register-form .el-input__prefix {
  left: 10px;
  font-size: 1.5rem;
  color: #999;
}

.register-select {
  width: 100%;
}

.register-select.el-select {
  height: 50px;
}

.register-select.el-select .el-input__inner {
  height: 50px;
}

.register-button {
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

.register-button:hover {
  background-color: #66b1ff;
}

.login-link,
.home-link {
  text-align: center;
  color: #666;
  margin-top: 1rem;
}

.login-link .el-button,
.home-link .el-button {
  color: #409eff;
}
</style>
