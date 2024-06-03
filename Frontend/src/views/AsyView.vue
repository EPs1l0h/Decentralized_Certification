<template>
  <div class="asy-view">
    <el-card class="algo-select" shadow="hover">
      <el-select v-model="method" placeholder="请选择加密算法">
        <el-option label="请选择非对称密码算法" value=""></el-option>
        <el-option label="SM2" value="SM2"></el-option>
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
      <el-input v-model="publicKey" placeholder="请输入公钥" :rows="2" />
      <el-input
        v-model="privateKey"
        placeholder="请输入私钥"
        class="mt-2"
        rows="2"
      />
      <el-button type="primary" @click="genKeyPair" class="mt-2" :rows="2"
        >生成密钥对</el-button
      >
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
.asy-view {
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
.mt-2 {
  margin-top: 10px;
}
</style>

<script setup lang="ts">
import { ref } from "vue";
import { Lock, Unlock } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import axios from "axios";

const inputText = ref<string>("");
const outputText = ref<string>("");
const publicKey = ref<string>("");
const privateKey = ref<string>("");
const method = ref<string>("请选择加密算法");
const loading = ref<boolean>(false);

const genKeyPair = async () => {
  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/asymmetric-encryption/gen-key",
      { method: method.value }
    );
    publicKey.value = data.publicKey;
    privateKey.value = data.privateKey;
    ElMessage.success("密钥对生成成功");
  } catch (error) {
    ElMessage.error("密钥对生成失败");
  } finally {
    loading.value = false;
  }
};

const encrypt = async () => {
  if (!inputText.value) {
    ElMessage.warning("请输入明文");
    return;
  }
  if (!publicKey.value) {
    ElMessage.warning("请输入公钥");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/asymmetric-encryption/encrypt",
      { message: inputText.value, key: publicKey.value, method: method.value }
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
  if (!privateKey.value) {
    ElMessage.warning("请输入私钥");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/asymmetric-encryption/decrypt",
      { message: inputText.value, key: privateKey.value, method: method.value }
    );
    outputText.value = data.message;
  } catch (error) {
    ElMessage.error("解密失败");
  } finally {
    loading.value = false;
  }
};
</script>
