<script setup lang="ts">
import Login from '@/components/Login.vue';
const loginVisible = ref(true)

const handleClick = () => {
  loginVisible.value = true
}

const handleCloseLogin = () => {
  loginVisible.value = false
}
</script>

<template>
  <div class="home">
    <el-container class="layout-container">
      <Login :visible="loginVisible" @close-login="handleCloseLogin" ></Login>
      <el-header class="header">
        <img id="logo" src="@/assets/eye.svg" />
        <el-button class="base-button header-button" @click="handleClick">登录</el-button>
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
