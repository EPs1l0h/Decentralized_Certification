<template>
  <div class="home">
    <el-row justify="center" align="middle" class="slogan">
      <el-col :span="24">
        <h1>去中心化</h1>
        <h2>基于区块链的身份管理系统</h2>
        <p>安全、透明、高效,为您的证书提供可靠的存储和验证方案。</p>
        <div class="buttons">
          <el-button
            type="primary"
            size="large"
            round
            @click="$router.push('/login')"
            >登录</el-button
          >
          <el-button size="large" round @click="$router.push('/register')"
            >注册</el-button
          >
        </div>
      </el-col>
    </el-row>
    <el-row justify="space-around" class="features">
      <el-col :span="7">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>安全可靠</span>
              <el-icon class="icon" color="#ff6b6b" :size="30"
                ><Lock
              /></el-icon>
            </div>
          </template>
          <div class="card-content">
            基于区块链技术,证书信息存储在分布式网络中,无法篡改,确保证书的真实性和可靠性。
          </div>
        </el-card>
      </el-col>
      <el-col :span="7">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>透明高效</span>
              <el-icon class="icon" color="#5ccfe6" :size="30"
                ><Sunny
              /></el-icon>
            </div>
          </template>
          <div class="card-content">
            证书的整个生命周期都记录在区块链上,可以随时查询和验证,提高证书管理的透明度和效率。
          </div>
        </el-card>
      </el-col>
      <el-col :span="7">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>易用灵活</span>
              <el-icon class="icon" color="#ff9a3c" :size="30"
                ><UserFilled
              /></el-icon>
            </div>
          </template>
          <div class="card-content">
            提供直观的 Web
            界面,用户可以方便地管理自己的证书,验证者也能快速验证证书的有效性。
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { Lock, Sunny, UserFilled } from "@element-plus/icons-vue";
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

.slogan {
  height: 50vh;
  background: linear-gradient(45deg, #ff6b6b, #5ccfe6);
  color: white;
}

.slogan h1 {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.slogan h2 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

.slogan p {
  font-size: 1.5rem;
  margin-bottom: 3rem;
}

.buttons .el-button {
  margin: 0 1rem;
}

.features {
  margin-top: 3rem;
}

.features .el-card {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 1.5rem;
  font-weight: bold;
}

.card-content {
  text-align: left;
}
</style>
