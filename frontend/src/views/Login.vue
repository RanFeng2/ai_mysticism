<template>
  <div class="container" v-if="!isAuthenticated">
    <!-- 注册界面 -->
    <div class="register">
      <h1>Register Now!</h1>
      <input v-model="username" placeholder="Enter username">
      <input v-model="password" type="password" placeholder="Enter password">
      <input v-model="email" placeholder="Enter email">
      <button @click="registerUser">Register</button>
    </div>
    <!-- 登录界面 -->
    <div class="login">
      <h1>Login</h1>
      <input v-model="loginUsername" placeholder="Enter username">
      <input v-model="loginPassword" type="password" placeholder="Enter password">
      <button @click="loginUser">Login</button>
      <button v-if="isAuthenticated" @click="logoutUser">Logout</button>
    </div>
  </div>
  <!-- 过去的占卜展示 -->
  <div v-else>
    <h1>Welcome, {{ user.Username }}!</h1>
    <div class="card-container">
      <div v-for="(divination, index) in all_result" :key="index" class="card">
        <h2>占卜{{index}}</h2>
        <p><strong>占卜日期：</strong>{{ divination.DivinationDate }}</p>
        <p><strong>占卜类型：</strong>{{ divination.DivinationType }}</p>
        <p><strong>问题：</strong>{{ divination.Question }}</p>
        <div v-html="divination.Result"></div>
      </div>
    </div>
</div>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue';
import { useRouter } from 'vue-router'
import { useStore } from 'vuex';

    const username = ref('');
    const password = ref('');
    const email = ref('');
    const loginUsername = ref('');
    const loginPassword = ref('');

    const store = useStore();
    const user = computed(() => store.getters.user);  
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    // console.log("[login.vue-beginning]user=", user)
    // console.log("[login.vue-beginning]isAuthenticated=", isAuthenticated)
    // console.log("[login.vue]",localStorage.getItem('user'))

    const all_result = ref([])

    // 异步函数loginUser用于处理用户登录逻辑
    // 登录，查询数据库
    async function loginUser() {
      // 定义登录接口URL
      const loginUrl = 'http://localhost:8000/login/';
      // 构建登录请求的数据对象，包含用户名、密码和空的邮箱字段
      const loginData = {
        user_name: loginUsername.value,
        PasswordHash: loginPassword.value,
        Email: "",
      };

      try {
        // 发送POST请求到登录接口
        const response = await fetch(loginUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(loginData),
        });

        // 如果响应状态不为200，抛出错误
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        // 保存到vuex
        const data = await response.json()
        const data_json_stringify = JSON.stringify(data.db_user)
        store.commit('setUser', data_json_stringify)

        // 在控制台打印
        // console.log("[login.vue]localStorage.getItem('user')=", computed(() => store.getters.user))
        // console.log("[login.vue]isAuthenticated.value=", computed(() => store.getters.isAuthenticated))
      } catch (error) {
        // 在控制台打印登录失败的错误信息
        console.error('[login]Login failed:', error);
      }

    }
    
    // 异步函数registerUser用于用户注册
    // 注册,数据库新增条目
    async function registerUser() {
      // 定义注册接口URL
      const registerUrl = 'http://localhost:8000/users/';
      // 构建用户数据对象，包含用户名、密码和邮箱
      const userData = {
        user_name: username.value,
        PasswordHash: password.value,
        Email: email.value,
      };

      try {
        // 发起POST请求，提交用户数据进行注册
        const response = await fetch(registerUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData),
        });

        // 如果响应状态不为200，抛出错误
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        // 解析响应的JSON数据，打印注册成功信息，并存储用户信息到本地存储
        const data = await response.json();
        console.log('User registered', data);
        // user.value = data.db_user;                                 //已经通过mutation修改了状态
        // localStorage.setItem('user', JSON.stringify(user.value));  //已经通过mutation修改了状态
        store.commit('setUser', JSON.stringify(data.db_user))

      } catch (error) {
        // 捕获注册过程中的任何错误并打印
        console.error('Registration failed:', error);
      }
    }

      // 退出登录，清除用户信息
      function logoutUser() {
        store.commit('logout');
    }


    // 异步函数listUserDivination用于用户查询对话
    async function listUserDivination() {
      
      if (isAuthenticated.value){
        const userid = user.value.UserId
        // console.log("[login.vue]userid=", userid)
      
      // 定义查询接口URL
      const queryUrl = 'http://localhost:8000/queryall/';
      // 构建用户数据对象，包含userid
      const queryData = {
        UserId: userid,
      };
      // 发起POST请求，提交用户id进行注册
      try {
        const response = await fetch(queryUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(queryData),
        });
        // 如果响应状态不为200，抛出错误
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        // 解析响应的JSON数据
        const data = await response.json();
        // 打印查询成功信息，并存储查询信息到本地存储
        console.log('Query success!!!', data);

        all_result.value = data.db_Divination

      } catch (error) {
        // 捕获查询过程中的任何错误并打印
        console.error('Query failed:', error);
      }
    }
    }

    onMounted(() => {
      listUserDivination()
    })
  
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
}

.register, .login {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 15px;
  width: 300px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}


</style>

