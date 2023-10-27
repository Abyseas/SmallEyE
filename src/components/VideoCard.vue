<script setup lang="ts">
  const url = 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
</script>
<template>
  <el-card class="video-card" :body-style="{ padding: '0px' }">
    <el-image :src="url" />
  </el-card>
</template>

<style lang="less" scoped>
  .video-card {
    width: 200px;
    border: none;
    border-radius: 12px;
  }
</style>
