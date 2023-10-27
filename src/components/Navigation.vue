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
    <el-menu class="navigation" router>
      <el-menu-item v-for="item in navList" :index="item.url">
        <div class="nav-item">
          <el-icon> <component :is="`icon-${item.icon}`"></component> </el-icon>
          <span>{{ item.label }}</span>
        </div>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<style lang="less" scoped>
  @import '@/styles/navigation.less';
</style>
