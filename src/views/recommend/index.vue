<script setup lang="ts">
  import { video } from '@/api/video'
  const videoListLen = ref(0)
  const videoList = ref<API.VideoInfo[]>([])

  const getVideoList = async (lastIdx: number) => {
    const videoResult = await video(lastIdx, 10)
    videoList.value = videoList.value.concat(videoResult.data)
    videoListLen.value = videoList.value.length
  }

  const handleReachEnd = () => {
    getVideoList(videoListLen.value)
  }

  onMounted(() => {
    getVideoList(videoListLen.value)
  })
</script>

<template>
  <div class="recommend-view">
    <VideoSwiper
      :videoList="videoList"
      :isMask="false"
      :activeIdx="0"
      @reachEnd="handleReachEnd"
    ></VideoSwiper>
  </div>
</template>

<style lang="less" scoped>
  .recommend-view {
    position: fixed;
    width: 88%;
    padding-right: 20px;
  }
</style>
