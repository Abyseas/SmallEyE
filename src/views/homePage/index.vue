<script setup lang="ts">
  import { video } from '@/api/video'
  import { Waterfall } from 'vue-waterfall-plugin-next'
  import SwiperMask from '@/components/SwiperMask.vue'
  import 'vue-waterfall-plugin-next/dist/style.css'
  const videoList = ref<API.VideoInfo[]>([])
  const getVideoList = async () => {
    const videoResult = await video()
    videoList.value = videoList.value.concat(videoResult.data.list)
  }

  const muted = ref(true)
  const activeIdx = ref(0)
  const showVideoSwiper = ref(false)

  const handleMutedChange = (event: Event) => {
    const player = event.target as HTMLAudioElement
    muted.value = player.muted
  }

  const handleClick = (index: number) => {
    console.log(index)
    activeIdx.value = index
    showVideoSwiper.value = true
  }

  const handleCloseVideoMask = () => {
    showVideoSwiper.value = false
  }

  getVideoList()
</script>

<template>
  <div class="home-page-container">
    <Waterfall :list="videoList" :width="300" v-infinite-scroll="getVideoList">
      <template #item="{ item, index }">
        <VideoCard
          :muted="muted"
          :video="item"
          @mutedChange="handleMutedChange"
          @click="handleClick(index)"
        ></VideoCard>
      </template>
    </Waterfall>
    <SwiperMask
      :videoList="videoList"
      :visible="showVideoSwiper"
      :activeIdx="activeIdx"
      @closeVideoMask="handleCloseVideoMask"
    ></SwiperMask>
  </div>
</template>

<style lang="less" scoped>
  @import '@/styles/homepage.less';
</style>
