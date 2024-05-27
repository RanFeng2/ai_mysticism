<script setup>
import {
  NInput, NButton, NCard, NDatePicker, NSelect, NFormItem,
  NInputNumber, NTabs, NTabPane, NDrawer, NDrawerContent
} from 'naive-ui'
import { watch, ref, onMounted } from "vue";
import MarkdownIt from 'markdown-it';
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';
import { useStorage } from '@vueuse/core';
import { Solar } from 'lunar-javascript'

import { useIsMobile } from '../utils/composables'
import About from '../components/About.vue'

import { DIVINATION_OPTIONS } from "../config/constants";
const isMobile = useIsMobile()

const state_jwt = useStorage('jwt')
const prompt = ref("");
const results = ref([]);  // 使用一个数组来存储所有结果
const tmp_result = ref("");
const prompt_type = useStorage("prompt_type", "tarot");
const menu_type = useStorage("menu_type", "divination");
const lunarBirthday = ref("");
const birthday = useStorage("birthday", "2000-08-17 00:00:00");
const loading = ref(false);
const API_BASE = import.meta.env.VITE_API_BASE || "";
const md = new MarkdownIt();
const showDrawer = ref(false)
const sex = ref("")
const surname = ref("")
const new_name_prompt = ref("")
const sexOptions = [
  { label: "男", value: "男" },
  { label: "女", value: "女" },
]
const plum_flower = useStorage("plum_flower", { num1: 0, num2: 0 })
const fate_body = useStorage("fate_body", { name1: "", name2: "" })

console.log("Script loaded");  // 确保脚本加载成功

const onSubmit = async () => {
  console.log("Submit clicked");  // 确保点击事件触发
  try {
    loading.value = true;
    console.log("Loading set to true"); // 确保按钮加载状态正确设置
    tmp_result.value = "";
    showDrawer.value = true;
    await fetchEventSource(`${API_BASE}/api/divination`, {
      method: "POST",
      body: JSON.stringify({
        prompt: prompt.value || "为我预测今日运势",
        prompt_type: prompt_type.value,
        birthday: birthday.value,
        new_name: {
          surname: surname.value,
          sex: sex.value,
          birthday: birthday.value,
          new_name_prompt: new_name_prompt.value
        },
        plum_flower: prompt_type.value == "plum_flower" ? plum_flower.value : null,
        fate: prompt_type.value == "fate" ? fate_body.value : null
      }),
      headers: {
        "Authorization": `Bearer ${state_jwt.value || "xxx"}`,
        "Content-Type": "application/json"
      },
      async onopen(response) {
        if (response.ok && response.headers.get('content-type') === EventStreamContentType) {
          return;
        } else if (response.status >= 400 && response.status < 500) {
          throw new Error(`${response.status} ${await response.text()}`);
        }
      },
      onmessage(msg) {
        if (msg.event === 'FatalError') {
          throw new FatalError(msg.data);
        }
        if (!msg.data) {
          return;
        }
        try {
          tmp_result.value += JSON.parse(msg.data);
        } catch (error) {
          console.error("Error parsing message data:", error);
        }
      },
      onclose() {
        try {
          const final_result = md.render(tmp_result.value);
          results.value.push(final_result);
          console.log("final_result:", final_result);
        } catch (error) {
          console.error("Error rendering final result:", error);
          results.value.push("占卜结果解析失败");
        }
        console.log("Connection closed");
        loading.value = false;
      },
      onerror(err) {
        console.log("Error occurred:", err.message);
        results.value.push(`占卜失败: ${err.message}`);
        loading.value = false;
      }
    });
  } catch (error) {
    console.error("Catch block error:", error);
    results.value.push(error.message || "占卜失败");
    loading.value = false;
  }
};

const computeLunarBirthday = (newBirthday) => {
  try {
    let date = new Date(newBirthday)
    let solar = Solar.fromYmdHms(
      date.getFullYear(), date.getMonth() + 1, date.getDate(),
      date.getHours(), date.getMinutes(), date.getSeconds());
    lunarBirthday.value = solar.getLunar().toFullString();
  } catch (error) {
    console.error(error)
    lunarBirthday.value = '转换失败'
  }
}

watch(birthday, async (newBirthday, oldBirthday) => {
  computeLunarBirthday(newBirthday)
})

const changeTab = async (delta) => {
  let curIndex = DIVINATION_OPTIONS.findIndex((option) => option.key === prompt_type.value);
  let newIndex = curIndex + delta;
  if (newIndex < 0) {
    newIndex = DIVINATION_OPTIONS.length - 1;
  } else if (newIndex >= DIVINATION_OPTIONS.length) {
    newIndex = 0;
  }
  prompt_type.value = DIVINATION_OPTIONS[newIndex].key;
}

onMounted(async () => {
  computeLunarBirthday(birthday.value)
});
</script>


<template>
  <div>
    <n-tabs v-model:value="prompt_type" type="card" animated placement="top">
      <n-tab-pane v-for="option in DIVINATION_OPTIONS" :key="option.key" :name="option.key" :tab="option.label">
        <n-card>
          <!-- 结果显示区域 -->
          <div class="result-container">
            <h3>占卜结果</h3>
            <div v-for="(result, index) in results" :key="index" v-html="result" class="result"></div>
          </div>
          <!-- 输入和操作区域 -->
          <div class="input-container" style="display: flex; align-items: center;">
            <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 3 }"
              placeholder="请输入您的问题" style="flex-grow: 1; margin-right: 8px;" />
            <n-button class="button" @click="onSubmit" type="primary" :disabled="loading">
              {{ loading ? "正在发送..." : "发送" }}
            </n-button>
          </div>
        </n-card>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>


<style scoped>
.button-container {
  display: flex;
  justify-content: center;
}

.button {
  margin: 10px;
}

.input-container {
  display: flex;
  align-items: center;
}

.result {
  text-align: left;
}
</style>
