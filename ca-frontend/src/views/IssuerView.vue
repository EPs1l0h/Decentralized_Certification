<!-- views/IssuerView.vue -->
<template>
  <div class="issuer-view">
    <el-row justify="center" class="header">
      <el-col :span="24">
        <h1>颁发者证书管理</h1>
        <p>为持有者颁发可验证的数字凭证。</p>
      </el-col>
    </el-row>
    <el-row justify="center" class="step-row">
      <el-col :span="20">
        <el-steps :active="step" finish-status="success">
          <el-step title="查看认证DID申请" />
          <el-step title="验证DID" />
          <el-step title="颁发VC" />
        </el-steps>
      </el-col>
    </el-row>
    <el-row justify="center">
      <el-col :span="12">
        <!-- 查看认证DID申请界面 -->
        <el-card v-if="step === 0" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>认证DID申请列表</span>
              <el-icon class="icon" color="#f6d365"><List /></el-icon>
            </div>
          </template>
          <el-table :data="requestList" style="width: 100%">
            <el-table-column prop="username" label="申请者"></el-table-column>
            <el-table-column prop="did" label="DID"></el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button type="primary" @click="handleRequest(scope.row)">
                  处理
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 验证DID界面 -->
        <el-card v-if="step === 1" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>验证DID</span>
              <el-icon class="icon" color="#fda085"><Checked /></el-icon>
            </div>
          </template>
          <p>正在向标识符注册机构验证DID: {{ selectedRequest.did }}</p>
          <el-button type="primary" @click="verifyDID" :loading="verifying">
            开始验证
          </el-button>
        </el-card>

        <!-- 颁发VC界面 -->
        <el-card v-if="step === 2" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>颁发VC</span>
              <el-icon class="icon" color="#67C23A"><Postcard /></el-icon>
            </div>
          </template>
          <el-form :model="vcForm" label-width="120px">
            <el-form-item label="声明内容">
              <el-input
                v-model="vcForm.credential_subject"
                type="textarea"
                :rows="3"
                placeholder="请输入声明内容"
              ></el-input>
            </el-form-item>
            <el-form-item label="证书类型">
              <el-input
                v-model="vcForm.vc_type"
                placeholder="请输入证书类型"
              ></el-input>
            </el-form-item>
            <el-form-item label="密钥ID">
              <el-input
                v-model="vcForm.kid"
                placeholder="请输入密钥ID"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="issueVC" :loading="issuing">
                颁发VC
              </el-button>
            </el-form-item>
          </el-form>
          <el-alert
            v-if="vcResult"
            :title="vcResult.title"
            :type="vcResult.type"
            :description="vcResult.vc"
            show-icon
            class="vc-result"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { List, Checked, Postcard } from "@element-plus/icons-vue";
import axios from "axios";
import API from "@/config/api";

const step = ref(0);
const selectedRequest = ref({});
const verifying = ref(false);
const issuing = ref(false);

interface Request {
  username: string;
  did: string;
}

const requestList = ref<Request[]>([]);

interface VCForm {
  credential_subject: string;
  vc_type: string;
  kid: string;
}

const vcForm = ref<VCForm>({
  credential_subject: "",
  vc_type: "",
  kid: "",
});

interface VCResult {
  title: string;
  type: "success" | "error";
  vc: string;
}

const vcResult = ref<VCResult | null>(null);

const getRequestList = async () => {
  try {
    const response = await axios.post(API.getWhoRequestVerifyDID);
    const { isValid, username, DID } = response.data;
    if (isValid) {
      requestList.value = [{ username, did: DID }];
      return true;
    }
  } catch (error) {
    console.error("Error fetching request list:", error);
  }
  return false;
};

const pollRequestList = async () => {
  const pollInterval = 3000; // 轮询间隔,单位毫秒

  const poll = async () => {
    const success = await getRequestList();
    if (success) {
      clearInterval(timer);
    }
  };

  const timer = setInterval(poll, pollInterval);
};

onMounted(async () => {
  await pollRequestList();
});

const handleRequest = async (request: Request) => {
  selectedRequest.value = request;
  step.value = 1;
};

const verifyDID = async () => {
  verifying.value = true;
  try {
    const response = await axios.post(API.reqeustVerifyDID, {
      DID: selectedRequest.value.did,
    });
    const { isValid } = response.data;
    if (isValid) {
      step.value = 2;
    } else {
      console.error("DID verification failed.");
    }
  } catch (error) {
    console.error("Error verifying DID:", error);
  }
  verifying.value = false;
};

const issueVC = async () => {
  issuing.value = true;
  try {
    const response = await axios.post(API.giveVCToHolder, {
      credential_subject: vcForm.value.credential_subject,
      vc_type: vcForm.value.vc_type,
      kid: vcForm.value.kid,
    });
    const { isValid, vc } = response.data;
    if (isValid) {
      vcResult.value = {
        title: "颁发成功",
        type: "success",
        vc: JSON.stringify(vc, null, 2),
      };
    } else {
      vcResult.value = {
        title: "颁发失败",
        type: "error",
        vc: "颁发VC失败,请重试。",
      };
    }
  } catch (error) {
    console.error("Error issuing VC:", error);
    vcResult.value = {
      title: "颁发失败",
      type: "error",
      vc: "颁发VC失败,请重试。",
    };
  }
  issuing.value = false;
};
</script>

<style scoped>
.issuer-view {
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
  background: linear-gradient(45deg, #f6d365, #fda085);
  color: white;
  padding: 2rem;
  border-radius: 4px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.step-row {
  margin-bottom: 2rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 1.25rem;
  font-weight: bold;
}

.card-header .icon {
  font-size: 1.5rem;
}

.vc-result {
  margin-top: 1.5rem;
}
</style>
