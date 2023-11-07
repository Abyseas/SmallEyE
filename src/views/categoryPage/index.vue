<script setup lang="ts">
  import { videoCategory } from '@/api/video'
  import { useRoute } from 'vue-router'
  import { Waterfall } from 'vue-waterfall-plugin-next'
  import SwiperMask from '@/components/SwiperMask.vue'
  import 'vue-waterfall-plugin-next/dist/style.css'

  const router = useRoute()
  const videoList = ref<API.VideoInfo[]>([])
  const videoListLen = ref(0)

  const initVideoList = async () => {
    const videoResult = await videoCategory(category.value, 0)
    videoList.value = videoResult.data
    videoListLen.value = videoList.value.length
  }

  const addVideoList = async (lastIdx: number) => {
    const videoResult = await videoCategory(category.value, lastIdx)
    videoList.value = videoList.value.concat(videoResult.data)
    videoListLen.value = videoList.value.length
  }
  const category = ref('')
  const muted = ref(true)
  const activeIdx = ref(0)
  const showVideoSwiper = ref(false)
  const waterfallRef = ref()

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

  const updateCategory = (value: string | string[]) => {
    category.value = value as string
    initVideoList()
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
  }, 100)

  watch(
    () => router.params.category,
    (value, oldValue) => {
      if (value !== oldValue) {
        updateCategory(value)
      }
    },
  )
  onMounted(() => {
    updateCategory(router.params.category)
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
  </div>
</template>

<style lang="less" scoped>
  @import '@/styles/homepage.less';
</style>
