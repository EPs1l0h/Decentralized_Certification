<template>
  <div class="asy-view">
    <el-card class="algo-select" shadow="hover">
      <el-select v-model="method" placeholder="请选择数字签名算法">
        <el-option label="请选择数字签名算法" value=""></el-option>
        <el-option label="SM2" value="SM2"></el-option>
        <el-option label="ECDSA" value="ECDSA"></el-option>
      </el-select>
    </el-card>

    <el-row :gutter="12">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span style="font-size: 14px">消息</span>
            </div>
          </template>
          <el-input
            v-model="inputText"
            :rows="12"
            type="textarea"
            placeholder="消息"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span style="font-size: 14px">签名</span>
            </div>
          </template>
          <el-input
            v-model="outputText"
            :rows="12"
            type="textarea"
            placeholder="签名"
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
      <el-button type="primary" @click="sign">
        <template #icon>
          <Edit />
        </template>
        签名
      </el-button>
      <el-button type="success" @click="verify">
        <template #icon>
          <Check />
        </template>
        验证签名
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
import { Edit, Check } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import axios from "axios";

const inputText = ref<string>("");
const outputText = ref<string>("");
const publicKey = ref<string>("");
const privateKey = ref<string>("");
const method = ref<string>("请选择数字签名算法");
const loading = ref<boolean>(false);

const genKeyPair = async () => {
  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/digital-signature/gen-key",
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

const sign = async () => {
  if (!inputText.value) {
    ElMessage.warning("请输入消息");
    return;
  }
  if (!privateKey.value) {
    ElMessage.warning("请输入私钥");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/digital-signature/sign",
      { message: inputText.value, key: privateKey.value, method: method.value }
    );
    outputText.value = data.message;
  } catch (error) {
    ElMessage.error("签名失败");
  } finally {
    loading.value = false;
  }
};

const verify = async () => {
  if (!inputText.value) {
    ElMessage.warning("请输入消息");
    return;
  }
  if (!outputText.value) {
    ElMessage.warning("请输入签名");
    return;
  }
  if (!publicKey.value) {
    ElMessage.warning("请输入公钥");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post(
      "http://localhost:8000/api/digital-signature/verify",
      {
        message: inputText.value,
        signature: outputText.value,
        key: publicKey.value,
        method: method.value,
      }
    );
    if (data.signatureValid) {
      ElMessage({
        message: "签名验证成功",
        type: "success",
      });
    } else {
      ElMessage({
        message: "签名验证失败",
        type: "error",
      });
    }
  } catch (error) {
    ElMessage.error("请求验证失败");
  } finally {
    loading.value = false;
  }
};
</script>
