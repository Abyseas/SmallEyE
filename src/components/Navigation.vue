<script setup lang="ts">
  const nav_list = [
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

  const category_nav_list = [
    {
      label: '生活',
      url: '/life',
      icon: 'life',
    },
    {
      label: '资讯',
      url: '/news',
      icon: 'news',
    },
    {
      label: '科技',
      url: '/tech',
      icon: 'tech',
    },
    {
      label: '知识',
      url: '/book',
      icon: 'book',
    },
    {
      label: '影视',
      url: '/movie',
      icon: 'movie',
    },
    {
      label: '时尚',
      url: '/fashion',
      icon: 'fashion',
    },
    {
      label: '美食',
      url: '/food',
      icon: 'food',
    },
    {
      label: '游戏',
      url: '/game',
      icon: 'game',
    },
    {
      label: '音乐',
      url: '/music',
      icon: 'music',
    },
    {
      label: '体育',
      url: '/sport',
      icon: 'sport',
    },
  ]
</script>

<template>
  <el-aside class="left-aside">
    <div class="navigation">
      <el-menu class="navigation" router>
        <el-menu-item v-for="item in nav_list" :index="item.url">
          <div class="nav-item">
            <el-icon> <component :is="`icon-${item.icon}`"></component> </el-icon>
            <span>{{ item.label }}</span>
          </div>
        </el-menu-item>
      </el-menu>
      <el-divider class="nav-divider"></el-divider>
      <el-menu class="navigation" router>
        <el-menu-item v-for="item in category_nav_list" :index="item.url">
          <div class="nav-item">
            <el-icon> <component :is="`icon-${item.icon}`"></component> </el-icon>
            <span>{{ item.label }}</span>
          </div>
        </el-menu-item>
      </el-menu>
    </div>
  </el-aside>
</template>

<style lang="less" scoped>
  @import '@/styles/navigation.less';
</style>
<style lang="less">
  .el-divider--horizontal.nav-divider {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
</style>
