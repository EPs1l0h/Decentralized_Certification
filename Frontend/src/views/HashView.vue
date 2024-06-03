<template>
  <div class="hash-view">
    <el-card class="algo-select" shadow="hover">
      <el-select v-model="method" placeholder="请选择哈希算法">
        <el-option label="请选择哈希算法" value=""></el-option>
        <el-option label="SM3" value="SM3"></el-option>
        <el-option label="SHA-256" value="SHA-256"></el-option>
      </el-select>
    </el-card>

    <el-row :gutter="12">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span style="font-size: 14px">输入消息</span>
            </div>
          </template>
          <el-input
            v-model="inputText"
            :rows="12"
            type="textarea"
            placeholder="请输入消息"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span style="font-size: 14px">哈希值</span>
            </div>
          </template>
          <el-input
            v-model="outputText"
            :rows="12"
            type="textarea"
            placeholder="哈希结果"
            readonly
          />
        </el-card>
      </el-col>
    </el-row>

    <div class="op-btn">
      <el-button type="primary" @click="hash">
        <template #icon>
          <Lock />
        </template>
        哈希
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.hash-view {
  max-width: 1000px;
  margin: 0 auto;
}
.algo-select {
  margin-bottom: 20px;
}
.op-btn {
  margin-top: 20px;
  text-align: center;
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
import { Lock } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import axios from "axios";

const inputText = ref<string>("");
const outputText = ref<string>("");
const method = ref<string>("请选择哈希算法");
const loading = ref<boolean>(false);

const hash = async () => {
  if (!inputText.value) {
    ElMessage.warning("请输入消息");
    return;
  }

  try {
    loading.value = true;
    const { data } = await axios.post("http://localhost:8000/api/hash", {
      message: inputText.value,
      method: method.value,
    });
    outputText.value = data.message;
  } catch (error) {
    ElMessage.error("哈希失败");
  } finally {
    loading.value = false;
  }
};
</script>
