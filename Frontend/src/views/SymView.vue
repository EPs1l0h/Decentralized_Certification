<template>
  <div class="sym-view">
    <el-card class="algo-select" shadow="hover">
      <el-select v-model="method" placeholder="请选择加密算法">
        <el-option label="请选择对称密码算法" value=""></el-option>
        <el-option label="AES" value="AES"></el-option>
        <el-option label="SM4" value="SM4"></el-option>
      </el-select>
    </el-card>

    <el-row :gutter="12">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span style="font-size: 14px">输入</span>
            </div>
          </template>
          <el-input
            v-model="inputText"
            :rows="12"
            type="textarea"
            placeholder="请输入明文/密文"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span style="font-size: 14px">输出</span>
            </div>
          </template>
          <el-input
            v-model="outputText"
            :rows="12"
            type="textarea"
            placeholder="加密/解密结果"
            readonly
          />
        </el-card>
      </el-col>
    </el-row>

    <el-card class="key-input" shadow="hover">
      <el-input v-model="key" placeholder="请输入密钥" />
    </el-card>

    <div class="op-btn">
      <el-button type="primary" @click="encrypt">
        <template #icon>
          <Lock />
        </template>
        加密
      </el-button>
      <el-button type="success" @click="decrypt">
        <template #icon>
          <Unlock />
        </template>
        解密
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.sym-view {
  max-width: 1000px;
  margin: 0 auto;
}
.algo-select {
  margin-bottom: 20px;
}
.key-input {
  margin-top: 20px;
}
.op-btn {
  margin-top: 20px;
  text-align: center;
}
.op-btn .el-button {
  width: 120px;
}
.op-btn .el-button {
  width: 120px;
  height: 40px;
  font-size: 16px;
}

.card-header {
  text-align: center;
}
</style>
<script setup lang="ts">
import { ref } from "vue";
import { Lock, Unlock } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import axios from "axios";
const inputText = ref<string>("");
const outputText = ref<string>("");
const key = ref<string>("");
const method = ref<string>("请选择加密算法");
const loading = ref<boolean>(false);

const encrypt = async () => {
  if (!inputText.value) {
    ElMessage.warning("请输入明文");
    return;
  }
  if (!key.value) {
    ElMessage.warning("请输入密钥");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/symmetric-encryption/encrypt",
      { message: inputText.value, key: key.value, method: method.value }
    );
    outputText.value = data.message;
  } catch (error) {
    ElMessage.error("加密失败");
  } finally {
    loading.value = false;
  }
};

const decrypt = async () => {
  if (!inputText.value) {
    ElMessage.warning("请输入密文");
    return;
  }
  if (!key.value) {
    ElMessage.warning("请输入密钥");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/symmetric-encryption/decrypt",
      { message: inputText.value, key: key.value, method: method.value }
    );
    outputText.value = data.message;
  } catch (error) {
    ElMessage.error("解密失败");
  } finally {
    loading.value = false;
  }
};
</script>
