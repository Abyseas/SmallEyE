<script setup lang="ts"></script>

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
  @import '@/styles/home.less';
</style>
