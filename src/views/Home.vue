<script setup lang="ts">
  import Navigation from '@/components/Navigation.vue'
</script>

<template>
  <div class="home">
    <el-container class="layout-container">
      <el-header class="header">
        <img id="logo" src="@/assets/eye.svg" />
        <el-button class="base-button">登录</el-button>
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

<style lang="less" scoped>
  .home {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    .layout-container {
      color: #dcebf0;
      background-color: #243c61;
      width: 100%;
      height: 100%;
    }

    .base-button {
      position: absolute;
      right: 20px;
      border: none;
      border-radius: 5px;
      background-color: #4b9194;
      color: #dcebf0;
      font-size: 14px;
      margin: 10px;
      &:hover {
        background-color: #409fc5;
      }
    }
    .header {
      margin: auto;
      height: 70px;
      display: flex;
      align-items: center;
      justify-content: center;
      #logo {
        position: absolute;
        left: 40px;
      }
    }
  }
</style>
