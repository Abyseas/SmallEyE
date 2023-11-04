<script setup lang="ts">
  import { video } from '@/api/video'
  const videoList = ref<API.VideoInfo[]>([])
  const getVideoList = async () => {
    const videoResult = await video()
    videoList.value = videoResult.data.list
  }

  getVideoList()
</script>

<template>
  <div class="recommend-view">
    <VideoSwiper :videoList="videoList" :isMask="false"></VideoSwiper>
  </div>
</template>

<style lang="less" scoped>
  .recommend-view {
    position: fixed;
    width: 88%;
    padding-right: 20px;
  }
</style>
