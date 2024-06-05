<script setup>
import {
  NGrid, NGi, NSpace, NAlert, NButton, NMessageProvider, NPageHeader,
  NConfigProvider, NGlobalStyle, NBackTop, zhCN, darkTheme
} from 'naive-ui'
import { onMounted, onBeforeUnmount, ref, computed, watch, createApp } from "vue";
import { useRouter } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { useStore } from 'vuex';

import App from './App.vue';
import router from './router'; 
const routerLocal = useRouter()

const store = useStore();
const user = computed(() => store.getters.user);  // 使用computed创建响应式的用户状态
const isAuthenticated = computed(() => store.getters.isAuthenticated)
console.log("[app.vue-beginning]user=", user)
console.log("[app.vue-beginning]isAuthenticated=", isAuthenticated)
console.log("[app.vue]",localStorage.getItem('user'))

const themeStorage = useStorage('theme', 'light')
const theme = computed(() => themeStorage.value == 'dark' ? darkTheme : null)

// 跳转到登录
function logIn() {
  // 将用户导航到登录页面以进行身份验证
  routerLocal.push('/login');
}

// 登出
function logOut() {
  isAuthenticated.value = false;
  user.value = null;
  store.commit(
    'setUser', 
     null,
  );
  routerLocal.push('/');
}

// 跳转到主页
function toHomePage(){
  routerLocal.push('/');
}

</script>

<template>
  <n-config-provider :locale="zhCN" :theme="theme">
    <n-global-style />
    <n-message-provider>
      <div class="container">
        <div class="main">
          <n-page-header :subtitle="''">
            <template #title>
              <h3>AI 神秘学</h3>
            </template>
            <template #extra>
              <n-space>
                <n-button type="primary" ghost tag="a" target="_blank" href="https://github.com/RanFeng2/ai_mysticism">
                  ☆ Github
                </n-button>
                <n-button @click="themeStorage = (themeStorage == 'dark' ? 'light' : 'dark')">
                  {{ themeStorage == 'dark' ? '☀亮色' : '🌙暗色' }}
                </n-button>
                <n-button type="primary" ghost @click="toHomePage">
                  🏠主页
                </n-button>
                <n-button v-if="isAuthenticated" @click="router.push('\login')">{{ user.Username }}</n-button>
                <n-button v-if="isAuthenticated" @click="logOut">登出</n-button>
                <n-button v-if="!isAuthenticated" type="primary" @click="logIn">登录</n-button>
              </n-space>
            </template>
            <template #footer>
              <n-alert v-if="isAuthenticated" type="success">
                你好, {{ user.Username }}
              </n-alert>
              <n-alert v-if="!isAuthenticated" type="warning">
                当前未登录
              </n-alert>
            </template>
          </n-page-header>
          <router-view :key="$route.path"></router-view>
        </div>
      </div>
    </n-message-provider>
    <n-back-top />
  </n-config-provider>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.main {
  width: 100%;
  max-width: 80%;
  text-align: center;
}
</style>