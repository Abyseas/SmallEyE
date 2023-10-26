<script setup lang="ts">
  const navList = [
    {
      label: '首页',
      url: '/home',
      icon: 'home',
    },
    {
      label: '推荐',
      url: '/',
      icon: 'sparkle',
    },
    {
      label: '热点',
      url: '/hot',
      icon: 'fire',
    },
    {
      label: '我的',
      url: '/my',
      icon: 'user',
    },
  ]
</script>

<template>
  <el-aside class="left-aside">
    <el-menu class="navigation">
      <el-menu-item v-for="(item, index) in navList" :key="index">
        <div class="nav-item">
          <el-icon> <component :is="`icon-${item.icon}`"></component> </el-icon>
          <span>{{ item.label }}</span>
        </div>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style type="less" scoped>
  .left-aside {
    width: 160px;
    .navigation {
      background-color: #243c61;
      border: none;

      .el-menu-item:hover {
        background-color: #243c61;
      }

      .nav-item {
        font-size: 14px;
        color: #dcebf0;
        border-radius: 5px;
        width: 70px;
        padding: 0px 10px;

        &active {
          background-color: #ffffff27;
        }
      }

      .nav-item:hover {
        background-color: #ffffff27;
      }
    }
  }
</style>
