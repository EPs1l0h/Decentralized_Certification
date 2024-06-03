<!-- HolderView.vue -->
<template>
  <div class="holder-dashboard">
    <!-- 持有者信息 -->
    <el-card class="holder-info">
      <template #header>
        <div class="card-header">
          <span>持有者信息</span>
          <el-icon class="icon" color="#409EFF"><UserFilled /></el-icon>
        </div>
      </template>
      <div class="info-item">
        <span class="label">用户名:</span>
        <span class="value">{{ holderInfo.userName }}</span>
      </div>
      <div class="info-item">
        <span class="label">DID:</span>
        <span class="value">{{ holderInfo.did }}</span>
      </div>
    </el-card>

    <!-- VC列表 -->
    <el-card class="certificate-list">
      <template #header>
        <div class="card-header">
          <span>VC列表</span>
          <el-button
            type="primary"
            @click="openApplyVCDialog"
            icon="el-icon-plus"
            class="apply-btn"
          >
            申请VC
          </el-button>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8" v-for="vc in vcList" :key="vc.id">
          <el-card shadow="hover">
            <div class="vc-info">
              <div class="vc-type">{{ vc.type[1] }}</div>
              <div class="vc-issuer">颁发者: {{ vc.issuer }}</div>
              <div class="vc-date">颁发时间: {{ vc.issuanceDate }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- VP请求列表 -->
    <el-card class="vp-request-list">
      <template #header>
        <div class="card-header">
          <span>VP请求列表</span>
          <el-icon class="icon" color="#67C23A"><Bell /></el-icon>
        </div>
      </template>
      <el-table :data="vpRequestList" style="width: 100%">
        <el-table-column prop="verifier" label="请求者"></el-table-column>
        <el-table-column prop="requestDate" label="请求时间"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" @click="handleVPRequest(scope.row)">
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 申请VC对话框 -->
    <el-dialog
      title="申请VC"
      v-model="applyVCDialogVisible"
      width="30%"
      @close="resetApplyVCForm"
    >
      <el-form :model="applyVCForm" label-width="100px">
        <el-form-item label="颁发者">
          <el-select v-model="applyVCForm.issuer" placeholder="请选择">
            <el-option
              v-for="issuer in issuers"
              :key="issuer.value"
              :label="issuer.label"
              :value="issuer.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请理由">
          <el-input
            type="textarea"
            v-model="applyVCForm.reason"
            :rows="3"
            placeholder="请输入申请理由"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="applyVCDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="applyVC">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Bell, UserFilled } from "@element-plus/icons-vue";
import {
  vcList as mockVCList,
  vpRequestList as mockVPRequestList,
} from "@/mock";

const vcList = ref(mockVCList);
const vpRequestList = ref(mockVPRequestList);

const holderInfo = ref({
  userName: "",
  did: "",
});

const applyVCDialogVisible = ref(false);

const issuers = [
  { value: "did:example:beijing", label: "北京VC" },
  { value: "did:example:london", label: "伦敦VC" },
  { value: "did:example:seoul", label: "汉城VC" },
];

const applyVCForm = ref({
  issuer: "",
  reason: "",
});

onMounted(async () => {
  await getHolderInfo();
});

const getHolderInfo = async () => {
  // 模拟从后端获取持有者信息
  const mockHolderInfo = {
    userName: "张三",
    did: "did:example:123456789abcdefghi",
  };
  holderInfo.value = mockHolderInfo;
};

const openApplyVCDialog = () => {
  applyVCDialogVisible.value = true;
};

const resetApplyVCForm = () => {
  applyVCForm.value = {
    issuer: "",
    reason: "",
  };
};

const applyVC = async () => {
  // 模拟调用后端API
  ElMessage.success("请求已发送，等待颁发者通过");
  applyVCDialogVisible.value = false;
  resetApplyVCForm();
};

const handleVPRequest = async (request) => {
  // 模拟处理VP请求
  await ElMessageBox.confirm(`是否同意 ${request.verifier} 的VP请求?`, "提示", {
    type: "warning",
  });
  ElMessage.success("已同意VP请求!");
  // 从VP请求列表中移除处理完的请求
  vpRequestList.value = vpRequestList.value.filter(
    (item) => item.id !== request.id
  );
};
</script>

<style scoped>
.holder-dashboard {
  max-width: 1200px;
  margin: 20px auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 20px;
  font-weight: bold;
}

.holder-info,
.certificate-list,
.vp-request-list {
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 10px;
}

.label {
  display: inline-block;
  width: 80px;
  font-weight: bold;
}

.vc-info {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.vc-type {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.vc-issuer,
.vc-date {
  color: #666;
}

.apply-btn {
  display: flex;
  align-items: center;
}
</style>
