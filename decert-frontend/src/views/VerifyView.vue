<template>
  <div class="verify-view">
    <el-row justify="center" class="header">
      <el-col :span="24">
        <h1>验证证书</h1>
        <p>提供安全、透明、高效的证书验证服务。</p>
      </el-col>
    </el-row>
    <el-row justify="center" class="step-row">
      <el-col :span="20">
        <el-steps :active="step" finish-status="success">
          <el-step title="发起验证请求" />
          <el-step title="持有者提交证书" />
          <el-step title="验证证书" />
        </el-steps>
      </el-col>
    </el-row>
    <el-row justify="center">
      <el-col :span="12">
        <!-- 发起验证请求界面 -->
        <el-card v-if="step === 0" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>发起验证请求</span>
              <el-icon class="icon" color="#f6d365"><Promotion /></el-icon>
            </div>
          </template>
          <el-form ref="requestForm" :model="requestForm" label-width="100px">
            <el-form-item label="持有者名称">
              <el-input
                v-model="holder_name"
                placeholder="请输入持有者的用户名或DID"
              ></el-input>
            </el-form-item>
            <el-form-item label="验证者名称">
              <el-input
                v-model="verify_name"
                placeholder="请输入持有者的用户名或DID"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="handleRequest"
                :loading="requesting"
              >
                <template #default> 发起请求 </template>
                <template #loading>
                  <div class="custom-loading">
                    <svg class="circular" viewBox="-10, -10, 50, 50">
                      <path
                        class="path"
                        d="
                          M 30 15
                          L 28 17
                          M 25.61 25.61
                          A 15 15, 0, 0, 1, 15 30
                          A 15 15, 0, 1, 1, 27.99 7.5
                          L 15 15
                        "
                        style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
                      />
                    </svg>
                  </div>
                </template>
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 持有者提交证书界面(省略) -->

        <!-- 验证证书界面 -->
        <el-card v-if="step === 2" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>验证证书</span>
              <el-icon class="icon" color="#fda085"><Stamp /></el-icon>
            </div>
          </template>
          <el-descriptions
            title="证书信息"
            :column="1"
            border
            :contentStyle="{
              'white-space': 'pre-wrap',
              'word-break': 'break-all',
            }"
          >
            <el-descriptions-item label="证书类型">
              {{ vcvp.type }}
            </el-descriptions-item>
            <el-descriptions-item label="证书内容">
              {{ JSON.stringify(vcvp, null, 2) }}
            </el-descriptions-item>
            <el-descriptions-item label="颁发者">
              {{ vcvp.issuer }}
            </el-descriptions-item>
            <el-descriptions-item label="颁发时间">
              {{ vcvp.issuanceDate }}
            </el-descriptions-item>
          </el-descriptions>
          <div class="verify-footer">
            <el-tooltip
              effect="dark"
              content="检查证书的有效性和真实性"
              placement="top"
            >
              <el-button
                type="primary"
                @click="handleVerify"
                :loading="verifying"
                class="verify-button"
              >
                验证证书
              </el-button>
            </el-tooltip>
            <el-alert
              v-if="verifyResult"
              :title="verifyResult.title"
              :type="verifyResult.type"
              :description="verifyResult.message"
              show-icon
              class="verify-result"
            />
          </div>
        </el-card>

        <!-- 验证成功界面 -->
        <el-card v-if="step === 3" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>验证成功</span>
              <el-icon class="icon" color="#67C23A"><SuccessFilled /></el-icon>
            </div>
          </template>
          <div class="success-content">
            <el-icon class="success-icon"><CircleCheckFilled /></el-icon>
            <h2>恭喜,您已成功完成证书验证!</h2>
            <p>
              通过对持有者提交的可验证声明(VP)的验证,您确认了该持有者身份的真实性和可信性。这为后续与其开展各种信任协作奠定了基础。
            </p>
            <p>
              基于可验证凭证体系,我们能够高效、可信地完成身份认证,同时保护个人隐私,推动多方协作。让我们共同见证价值互联网时代的到来!
            </p>
            <el-button type="primary" @click="reset">继续验证</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onUnmounted } from "vue";
import { Promotion, Stamp } from "@element-plus/icons-vue";
import api from "@/config/api";

const requestForm = reactive({
  verifyName: "",
});

const holder_name = ref("");
const verify_name = ref("");

const step = ref(0);
const requesting = ref(false);

interface VCVP {
  type: string;
  credentialSubject: any;
  issuer: string;
  issuanceDate: string;
}

const vcvp = ref<VCVP | null>(null);
const verifying = ref(false);

interface VerifyResult {
  title: string;
  type: "success" | "error";
  message: string;
}

const verifyResult = ref<VerifyResult | null>(null);

let pollTimer: number | null = null;

const handleRequest = async () => {
  requesting.value = true;
  requestForm.verifyName = verify_name.value;

  try {
    await fetch(api.askHolder, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ verify_username: verify_name.value }),
    });

    step.value = 1;

    const pollVP = async () => {
      const response = await fetch(api.checkVP, {
        method: "POST",
      });
      const data = await response.json();

      if (data.vp) {
        vcvp.value = data.vp;
        step.value = 2;
      } else {
        pollTimer = setTimeout(pollVP, 10000);
      }
    };

    await pollVP();
  } catch (error) {
    console.error("请求错误:", error);
  }

  requesting.value = false;
};

const handleVerify = async () => {
  verifying.value = true;

  try {
    const response = await fetch(api.verifyVP, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ vp: vcvp.value }),
    });
    const data = await response.json();

    if (data.msg) {
      verifyResult.value = {
        title: "验证成功",
        type: "success",
        message: data.msg,
      };
    } else {
      verifyResult.value = {
        title: "验证失败",
        type: "error",
        message: "VC/VP验证失败,该证书无效。",
      };
    }
  } catch (error) {
    console.error("验证错误:", error);
    verifyResult.value = {
      title: "验证失败",
      type: "error",
      message: "验证过程中发生错误。",
    };
  }

  verifying.value = false;
  step.value = 3;
};

onUnmounted(() => {
  if (pollTimer) {
    clearTimeout(pollTimer);
  }
});
</script>
<style scoped>
.verify-view {
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

.verify-footer {
  text-align: center;
  margin-top: 2rem;
}

.verify-button {
  background: linear-gradient(45deg, #f6d365, #fda085);
  border: none;
  color: white;
  font-size: 1.25rem;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.verify-button:hover {
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.verify-result {
  margin-top: 1.5rem;
  text-align: center;
}

/* loading动画 */
.custom-loading .circular {
  width: 20px;
  height: 20px;
  animation: loading-rotate 2s linear infinite;
}

.custom-loading .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-white);
  stroke-linecap: round;
}

@keyframes loading-rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -120px;
  }
}
</style>
