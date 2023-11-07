<script setup lang="ts">
  import Login from '@/components/Login.vue'
  import { storage } from '@/utils/common'
  import { ElMessage } from 'element-plus'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const loginVisible = ref(false)
  const isLogin = ref(false)
  const username = ref('')
  const handleClick = () => {
    loginVisible.value = true
  }

  const handleCloseLogin = () => {
    loginVisible.value = false
  }

  const handleConfirm = () => {
    storage.remove('token')
    storage.remove('username')
    storage.remove('tokenStartTime')
    updateLoginState()
    //跳转到首页
    router.push({ path: '' })
    ElMessage({
      message: '用户已退出',
      type: 'error',
    })
  }

  const handleLogin = () => {
    isLogin.value = true
    updateLoginState()
  }

  const updateLoginState = () => {
    const token = storage.get('token')
    if (token) {
      isLogin.value = true
      loginVisible.value = false
      username.value = storage.get('username') as string
    } else {
      isLogin.value = false
      loginVisible.value = true
      username.value = ''
    }
  }
  onMounted(() => {
    updateLoginState()
  })
</script>

<template>
  <div class="home">
    <el-container class="layout-container">
      <Login
        :visible="loginVisible"
        @close-login="handleCloseLogin"
        @loginSuccess="handleLogin"
      ></Login>
      <el-header class="header">
        <img id="logo" src="@/assets/eye.svg" />
        <el-button v-if="!isLogin" class="base-button header-button" @click="handleClick"
          >登录</el-button
        >
        <div class="header-username">
          <el-icon v-if="username.length"> <component :is="`icon-user`"></component> </el-icon>
          {{ username }}</div
        >
        <el-popconfirm
          class="exist-popconfirm"
          width="200"
          confirm-button-text="确认"
          cancel-button-text="取消"
          title="请再次点击确认退出"
          @confirm="handleConfirm"
        >
          <template #reference>
            <el-button v-if="isLogin" class="base-button header-button">退出</el-button>
          </template>
        </el-popconfirm>
      </el-header>
      <el-container>
        <Navigation></Navigation>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style lang="less">
  @import '@/styles/home.less';
</style>
