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
import api from "@/config/api"; // 引入全局配置文件

const vcList = ref([]);
const vpRequestList = ref([]);

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
  await getVCList();
  await getVPRequestList();
});

const getHolderInfo = async () => {
  try {
    const response = await fetch(api.getHolderInfo);
    const data = await response.json();
    if (data.isValid) {
      holderInfo.value = {
        userName: data.username,
        did: data.DID,
      };
    } else {
      ElMessage.error("获取持有者信息失败");
    }
  } catch (error) {
    console.error("获取持有者信息失败:", error);
    ElMessage.error("获取持有者信息失败");
  }
};

const getVCList = async () => {
  try {
    const response = await fetch(api.holderRequestVC);
    const data = await response.json();
    if (data.isValid) {
      vcList.value = data.VC;
    } else {
      ElMessage.error("获取VC列表失败");
    }
  } catch (error) {
    console.error("获取VC列表失败:", error);
    ElMessage.error("获取VC列表失败");
  }
};

const getVPRequestList = async () => {
  try {
    const response = await fetch(api.getBeAskedVPList, {
      method: "POST",
    });
    const data = await response.json();
    if (data.isValid) {
      vpRequestList.value = data.VC;
    } else {
      ElMessage.error("获取VP请求列表失败");
    }
  } catch (error) {
    console.error("获取VP请求列表失败:", error);
    ElMessage.error("获取VP请求列表失败");
  }
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
  try {
    const response = await fetch(api.requestAuthenticateDID, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(applyVCForm.value),
    });
    const data = await response.json();
    if (data.isValid) {
      ElMessage.success("请求已发送，等待颁发者通过");
      applyVCDialogVisible.value = false;
      resetApplyVCForm();
    } else {
      ElMessage.error("申请VC失败");
    }
  } catch (error) {
    console.error("申请VC失败:", error);
    ElMessage.error("申请VC失败");
  }
};

const handleVPRequest = async (request) => {
  try {
    await ElMessageBox.confirm(
      `是否同意 ${request.verifier} 的VP请求?`,
      "提示",
      {
        type: "warning",
      }
    );
    const response = await fetch(api.holderToVerifier, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: request.verifier }),
    });
    const data = await response.json();
    if (data.isValid) {
      ElMessage.success("已同意VP请求!");
      // 从VP请求列表中移除处理完的请求
      vpRequestList.value = vpRequestList.value.filter(
        (item) => item.id !== request.id
      );
    } else {
      ElMessage.error("处理VP请求失败");
    }
  } catch (error) {
    console.error("处理VP请求失败:", error);
    ElMessage.error("处理VP请求失败");
  }
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
