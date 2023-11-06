<script setup lang="ts">
  import { video } from '@/api/video'
  import { Waterfall } from 'vue-waterfall-plugin-next'
  import SwiperMask from '@/components/SwiperMask.vue'
  import VideoSkeleton from '@/components/VideoSkeleton.vue'
  import { skeletonList } from '@/utils/common'
  import 'vue-waterfall-plugin-next/dist/style.css'
  const videoList = ref<API.VideoInfo[]>([])

  const videoListLen = ref(0)
  const getVideoList = async (lastIdx: number) => {
    const videoResult = await video(lastIdx)
    if (loading.value === true) {
      loading.value = false
    }
    videoList.value = videoList.value.concat(videoResult)
    videoListLen.value = videoList.value.length
  }
  const muted = ref(true)
  const activeIdx = ref(0)
  const showVideoSwiper = ref(false)
  const loading = ref(true)
  const waterfallRef = ref()

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

  const handleReachEnd = () => {
    getVideoList(videoListLen.value)
  }

  const debounce = (func: Function, delay: number) => {
    let timer: any
    return function () {
      if (timer) {
        clearTimeout(timer)
      }

      timer = setTimeout(() => {
        console.log('func')
        func()
      }, delay)
    }
  }
  const handleProgress = debounce(() => {
    console.log('renderer')
    waterfallRef.value.renderer()
  }, 1000)

  onMounted(() => {
    setTimeout(() => {
      getVideoList(videoListLen.value)
    }, 1000)
  })
</script>

<template>
  <div
    class="home-page-container"
    v-infinite-scroll="
      () => {
        getVideoList(videoListLen)
      }
    "
    :infinite-scroll-immediate="false"
  >
    <el-skeleton style="display: flex; flex-wrap: wrap" :loading="loading" animated>
      <template #template>
        <Waterfall :list="skeletonList" :width="300">
          <template #item>
            <VideoSkeleton />
          </template>
        </Waterfall>
      </template>
      <template #default>
        <Waterfall :list="videoList" :width="300" ref="waterfallRef">
          <template #item="{ item, index }">
            <VideoCard
              :muted="muted"
              :video="item"
              @mutedChange="handleMutedChange"
              @click="handleClick(index)"
              @progress="handleProgress"
            ></VideoCard>
          </template>
        </Waterfall>
        <SwiperMask
          :videoList="videoList"
          :visible="showVideoSwiper"
          :activeIdx="activeIdx"
          @closeVideoMask="handleCloseVideoMask"
          @reachEnd="handleReachEnd"
        ></SwiperMask>
      </template>
    </el-skeleton>
  </div>
</template>

<style lang="less" scoped>
  @import '@/styles/homepage.less';
</style>
