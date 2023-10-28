<script setup lang="ts">
  import { video } from '@/api/video'
  import { Waterfall } from 'vue-waterfall-plugin-next'
  import 'vue-waterfall-plugin-next/dist/style.css'
  const videoList = ref<API.VideoInfo[]>([])
  const getVideoList = async () => {
    const videoResult = await video()
    videoList.value = videoResult.data.list
  }

  const muted = ref(true)

  const handleMutedChange = (event: Event) => {
    const player = event.target as HTMLAudioElement
    muted.value = player.muted
  }
  getVideoList()
</script>

<template>
  <div class="home-page-container">
    <Waterfall :list="videoList" :width="300">
      <template #item="{ item }">
        <VideoCard :muted="muted" :video="item" @mutedChange="handleMutedChange"></VideoCard>
      </template>
    </Waterfall>
  </div>
</template>

<style lang="less" scoped>
  @import '@/styles/homepage.less';
</style>
