<script setup lang="ts"></script>

<template>
  <router-view></router-view>
</template>

<style lang="less" scoped>
  #app {
    padding: 0;
    margin: 0;
  }

  body {
    background-color: #161722;
  }

  // 隐藏滚动条
  ::-webkit-scrollbar {
    width: 0 !important;
    height: 0 !important;
  }
</style>
