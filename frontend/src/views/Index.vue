<script setup>
import {
  NInput, NButton, NCard, NDatePicker, NSelect, NFormItem,
  NInputNumber, NTabs, NTabPane, NDrawer, NDrawerContent,
  NAvatar
} from 'naive-ui'
import { watch, ref, onMounted, onBeforeUnmount, computed} from "vue";
import MarkdownIt from 'markdown-it';
import { useRouter } from 'vue-router'
import { useStore } from 'vuex';
import { useStorage } from '@vueuse/core';
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source';
import { Solar } from 'lunar-javascript'
import { useIsMobile } from '../utils/composables'
import About from '../components/About.vue'
import { DIVINATION_OPTIONS } from "../config/constants";

const isMobile = useIsMobile()
const state_jwt = useStorage('jwt')
const prompt = ref("");
const conversations = ref([]);  // 使用一个数组来存储所有对话
const tmp_result = ref("");
const prompt_type = useStorage("prompt_type", "tarot");
const menu_type = useStorage("menu_type", "divination");
const lunarBirthday = ref("");
const birthday = useStorage("birthday", "2000-08-17 00:00:00");
const loading = ref(false);


const API_BASE = "";
// console.log("[index.vue]API_BASE",API_BASE)

const md = new MarkdownIt();
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

const store = useStore();
const user = computed(() => store.getters.user);  // 使用computed创建响应式的用户状态
const isAuthenticated = computed(() => store.getters.isAuthenticated)
console.log("[index.vue-beginning]user=", user)
console.log("[index.vue-beginning]isAuthenticated=", isAuthenticated)
console.log("[index.vue]",localStorage.getItem('user'))

const onSubmit = async () => {
  if (loading.value) return;  // 防止重复提交
  loading.value = true;
  try {
    console.log("Loading set to true"); // 确保按钮加载状态正确设置
    tmp_result.value = "";
    const userPrompt = prompt.value;
    prompt.value = "";  // 清空输入框
    await fetchEventSource(`${API_BASE}/api/divination`, {
      method: "POST",
      body: JSON.stringify({
        prompt: userPrompt || "如上",
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
          throw new Error("Fatal error occurred: " + msg.data);
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
          conversations.value.push({
            prompt: userPrompt,
            response: final_result
          });
          console.log("final_result:", final_result)

        } catch (error) {
          console.error("Error rendering final result:", error);
          conversations.value.push({
            prompt: userPrompt,
            response: "占卜结果解析失败"
          });
        }
        console.log("Connection closed");
        loading.value = false;
      },
      onerror(err) {
        console.log("Error occurred:", err.message);
        if (conversations.value.length === 0  || conversations.value[conversations.value.length - 1].response.indexOf('占卜失败') === -1) {
          conversations.value.push({
            prompt: userPrompt,
            response: `占卜失败: ${err.message}`
          });
        }
        loading.value = false;
      }
    });
  } catch (error) {
    console.error("Catch block error:", error);
    if (conversations.value.length === 0  || conversations.value[conversations.value.length - 1].response.indexOf('占卜失败') === -1) {
      conversations.value.push({
        prompt: userPrompt,
        response: error.message || "占卜失败"
      });
    }
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

const changeTab = async (delta) => {
  // 清空prompt
  prompt.value = "";
  // 清空对话记录
  conversations.value = [];
  // 更新当前的Index
  let curIndex = DIVINATION_OPTIONS.findIndex((option) => option.key === prompt_type.value);
  let newIndex = curIndex + delta;
  if (newIndex < 0) {
    newIndex = DIVINATION_OPTIONS.length - 1;
  } else if (newIndex >= DIVINATION_OPTIONS.length) {
    newIndex = 0;
  }
  // console.log("curIndex=", curIndex)
  prompt_type.value = DIVINATION_OPTIONS[curIndex].key;
  console.log("prompt_type.value=", prompt_type.value)
}

const updateBirthdayPrompt = (newBirthday) => {
  prompt.value = `我的生日是：${newBirthday}`;
};

const updateNewNamePrompt = (newSurname, newSex, newBirthday, newNamePrompt) => {
  prompt.value = `宝宝的姓氏是：${newSurname}， 宝宝的性别是：${newSex}， 宝宝的生日是：${newBirthday}， 附加信息：${newNamePrompt}`;
};

const updatePlumFlowerPrompt = (newNum1, newNum2) => {
  prompt.value = `我选择的数字1是：${newNum1}， 数字2是：${newNum2}`;
};


watch([prompt_type, birthday, surname, sex, new_name_prompt, plum_flower], ([newPromptType, newBirthday, newSurname, newSex, newNamePrompt, newPlumFlower], [oldPromptType, oldBirthday, oldSurname, oldSex, oldNamePrompt, oldPlumFlower]) => {
  computeLunarBirthday(newBirthday)
  if (newPromptType == 'birthday'){
    if (newBirthday !== oldBirthday) {
      updateBirthdayPrompt(newBirthday)
    }
  }

  if (newPromptType == 'new_name'){
    if (newSurname !== oldSurname || newSex !== oldSex || newBirthday !== oldBirthday || newNamePrompt !== oldNamePrompt) {
      updateNewNamePrompt(newSurname, newSex, newBirthday, newNamePrompt)
    }
  }

  if (newPromptType == 'plum_flower'){
    console.log('Checking Plum Flower:', newPlumFlower, oldPlumFlower);
    updatePlumFlowerPrompt(newPlumFlower.num1, newPlumFlower.num2)
  }

}, { deep: true })

</script>


<template>
  <div>
    <n-tabs v-model:value="prompt_type" type="card" animated placement="top" @update:value="changeTab">
      <!-- 在移动端显示左右箭头，用于切换占卜类型 -->
      <template v-if="isMobile" #prefix>
        <n-button @click="changeTab(-1)">←</n-button>
      </template>
      <template v-if="isMobile" #suffix>
        <n-button @click="changeTab(1)">→</n-button>
      </template>
      <!-- 根据不同的占卜类型，显示不同的输入组件 -->
      <n-tab-pane v-for="option in DIVINATION_OPTIONS" :key="option.key" :name="option.key" :tab="option.label">
        <n-card>
          <!-- 欢迎语显示区域 -->
          <div class="conversation-container">
            <!-- 塔罗牌占卜输入区域 -->
            <div v-if="prompt_type == 'tarot'" class="conversation">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-content ai">
                <div v-html="option.welcome_messages"></div>
              </div>
            </div>
            <!-- 生日占卜输入区域 -->
            <div v-if="prompt_type == 'birthday'">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-wrap">
                <!-- 欢迎语 -->
                <div class="conversation-content ai">
                  <div v-html="option.welcome_messages"></div>
                </div>
                <!-- 生日输入部分 -->
                <div class="additional-input-wrap">
                  <n-form-item label="生日" label-placement="left" class="centered">
                    <n-date-picker v-model:formatted-value="birthday" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" />
                  </n-form-item>
                  <n-form-item label="农历" label-placement="left" class="centered">
                    <p>{{ lunarBirthday }}</p>
                  </n-form-item>
                </div>
              </div>
            </div>
            <!-- 测名占卜输入区域 -->
            <div v-if="prompt_type == 'name'">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-wrap">
                <!-- 欢迎语 -->
                <div class="conversation-content ai">
                  <div v-html="option.welcome_messages"></div>
                </div>
              </div>
            </div>
            <!-- 起名占卜输入区域 -->
            <div v-if="prompt_type == 'new_name'">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-wrap">
                <!-- 欢迎语 -->
                <div class="conversation-content ai">
                  <div v-html="option.welcome_messages"></div>
                </div>
              </div>
                <!-- 起名信息输入部分 -->
                <div class="additional-input-wrap">
                  <n-form-item label="姓氏" label-placement="left">
                    <n-input v-model:value="surname" type="text" maxlength="4" placeholder="请输入姓氏" />
                  </n-form-item>
                  <n-form-item label="性别" label-placement="left" >
                    <n-select v-model:value="sex" :options="sexOptions" size="large" />
                  </n-form-item>
                  <n-form-item label="生日" label-placement="left">
                    <n-date-picker v-model:formatted-value="birthday" value-format="yyyy-MM-dd HH:mm:ss" type="datetime" />
                  </n-form-item>
                  <n-form-item label="附加" label-placement="left">
                    <n-input v-model:value="new_name_prompt" type="text" maxlength="20" placeholder="" />
                  </n-form-item>
                  <p>农历: {{ lunarBirthday }}</p>
                </div>
            </div>
            <!-- 梦境占卜输入区域 -->
            <div v-if="prompt_type == 'dream'">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-wrap">
                <!-- 欢迎语 -->
                <div class="conversation-content ai">
                  <div v-html="option.welcome_messages"></div>
                </div>
              </div>
            </div>
            <!-- 梅花易数占卜输入区域 -->
            <div v-if="prompt_type == 'plum_flower'">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-wrap">
                <!-- 欢迎语 -->
                <div class="conversation-content ai">
                  <div v-html="option.welcome_messages"></div>
                </div>
              </div>
              <!-- 数字输入区域 -->
              <div class="additional-input-wrap">
                <n-form-item label="数字一" label-placement="left">
                  <n-input-number v-model:value="plum_flower.num1" :min="0" :max="1000" />
                </n-form-item>
                <n-form-item label="数字二" label-placement="left">
                  <n-input-number v-model:value="plum_flower.num2" :min="0" :max="1000" />
                </n-form-item>
              </div>
            </div>
            <!-- 缘分占卜输入区域 -->
            <div v-if="prompt_type == 'fate'">
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain" 
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-wrap">
                <!-- 欢迎语 -->
                <div class="conversation-content ai">
                  <div v-html="option.welcome_messages"></div>
                </div>
              </div>
              <div style="display: inline-block;">
                <h4>缘分是天定的，幸福是自己的。</h4>
                <p>想知道你和 ta 有没有缘分呢，编辑“姓名1” “姓名2”，然后点击“一键预测”。</p>
                <p>如郭靖 黄蓉，然后点击一键预测。 就能查看你和 ta 的缘分了。</p>
                <n-form-item label="姓名1" label-placement="left">
                  <n-input v-model:value="fate_body.name1" round maxlength="40" />
                </n-form-item>
                <n-form-item label="姓名2" label-placement="left">
                  <n-input v-model:value="fate_body.name2" round maxlength="40" />
                </n-form-item>
              </div>
            </div>
            <!-- 对话显示区域 -->
            <div v-for="(conversation, index) in conversations" :key="index" class="conversation">
              <div class="conversation-item user">
                <n-avatar round :size="large" object-fit="contain" 
                  src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
                <p><strong>用户</strong></p>
              </div>
              <div class="conversation-content user">
                <div v-html="conversation.prompt"></div>
              </div>
              <div class="conversation-item ai">
                <n-avatar round :size="large" object-fit="contain"
                  src="tarot-200x200.jpg" />
                <p><strong>AI占卜师</strong></p>
              </div>
              <div class="conversation-content ai">
                <div v-html="conversation.response"></div>
              </div>
            </div>
          </div>
          <!-- 输入和操作区域 -->
          <div class="input-container" style="display: flex; align-items: center;">
            <n-input v-model:value="prompt" type="textarea" round maxlength="40" :autosize="{ minRows: 3 }"
              placeholder="请根据提示输入" style="flex-grow: 1; margin-right: 8px;" />
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

.conversation-container {
  text-align: left;
  margin-bottom: 10px;
}

.conversation-item {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.conversation-item.ai {
  flex-direction: row;
  margin-right: 10px;
}

.conversation-item.user {
  flex-direction: row-reverse;
  margin-left: 10px;
}

.conversation-item.ai p{
  margin-left: 10px;
}

.conversation-item.user p{
  margin-right: 10px;
}

.conversation-content {
  display: flex;
  align-items: flex-start;
  margin-top: 5px;
}

.conversation-content.ai {
  flex-direction: row;
  margin-left: 20px;
  margin-right: 10%;
  background-color: #211100;
  color: white;
  padding: 10px;
  border-radius: 5px;
}

.conversation-content.user {
  flex-direction: row-reverse;
  margin-right: 20px;
  margin-left: 60%;
  background-color: #f0f0f0;
  color: #333;
  padding: 10px;
  border-radius: 5px;
}

.conversation p {
  margin: 0;
}

.conversation div {
  margin-top: 5px;
}

.conversation-wrap {
  /* 如果需要，可以添加一些通用样式，比如外边距或内边距 */
  /* margin-left: 20px;
  margin-right: 10%;
  background-color: #211100;
  color: white;
  padding: 10px;
  border-radius: 5px; */
}

.additional-input-wrap {
  /* 确保生日输入部分从新的一行开始 */
  margin-top: 16px; /* 或其他您认为合适的间距 */
}

.n-form-item.centered {
  display: flex;
  align-items: center;
}




</style>
