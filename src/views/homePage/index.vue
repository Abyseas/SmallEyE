<script setup lang="ts">
  import { video, hotVideo } from '@/api/video'
  import { useRoute } from 'vue-router'
  import { Waterfall } from 'vue-waterfall-plugin-next'
  import SwiperMask from '@/components/SwiperMask.vue'
  import VideoSkeleton from '@/components/VideoSkeleton.vue'
  import { skeletonList } from '@/utils/common'
  import 'vue-waterfall-plugin-next/dist/style.css'
  const videoList = ref<API.VideoInfo[]>([])
  const router = useRoute()
  const videoListLen = ref(0)

  const initVideoList = async () => {
    let videoResult
    if (isHot.value) {
      videoResult = await hotVideo(0)
    } else {
      videoResult = await video(0)
    }

    if (loading.value === true) {
      loading.value = false
    }
    videoList.value = videoResult.data
    videoListLen.value = videoList.value.length
  }

  const addVideoList = async (lastIdx: number) => {
    let videoResult
    if (isHot.value) {
      videoResult = await hotVideo(lastIdx)
    } else {
      videoResult = await video(lastIdx)
    }

    videoList.value = videoList.value.concat(videoResult.data)
    videoListLen.value = videoList.value.length
  }
  const muted = ref(true)
  const activeIdx = ref(0)
  const isHot = ref(false)
  const showVideoSwiper = ref(false)
  const loading = ref(true)
  const waterfallRef = ref()

  const updateIsHot = (param: string | string[]) => {
    if (param === 'hot') {
      isHot.value = true
    } else {
      isHot.value = false
    }
    loading.value = true
    initVideoList()
  }

  const handleMutedChange = (event: Event) => {
    const player = event.target as HTMLAudioElement
    muted.value = player.muted
  }

  const handleClick = (index: number) => {
    activeIdx.value = index
    showVideoSwiper.value = true
  }

  const handleCloseVideoMask = () => {
    showVideoSwiper.value = false
  }

  const handleReachEnd = () => {
    addVideoList(videoListLen.value)
  }

  const debounce = (func: Function, delay: number) => {
    let timer: any
    return function () {
      if (timer) {
        clearTimeout(timer)
      }

      timer = setTimeout(() => {
        func()
      }, delay)
    }
  }
  const handleProgress = debounce(() => {
    waterfallRef.value.renderer()
  }, 1000)

  watch(
    () => router.params.hot,
    (value, oldValue) => {
      if (value !== oldValue) {
        updateIsHot(value)
      }
    },
  )

  onMounted(() => {
    updateIsHot(router.params.hot)
    setTimeout(() => {
      initVideoList()
    }, 1000)
  })
</script>

<template>
  <div
    class="home-page-container"
    v-infinite-scroll="
      () => {
        addVideoList(videoListLen)
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
