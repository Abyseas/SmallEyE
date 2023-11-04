<script setup lang="ts">
  import { Close } from '@element-plus/icons-vue'
  const props = defineProps<{
    visible: boolean
    videoList: API.VideoInfo[]
    activeIdx: number
  }>()
  const emit = defineEmits(['closeVideoMask'])
  const videoList = ref<API.VideoInfo[]>(props.videoList)
  const visible = ref(props.visible)
  const handleClose = () => {
    visible.value = false
    emit('closeVideoMask')
  }

  watch(
    () => props.visible,
    (value: boolean) => {
      if (value === true) {
        visible.value = true
      }
    },
  )

  watch(
    () => props.videoList,
    (value: API.VideoInfo[]) => {
      videoList.value = value
    },
  )
</script>

<template>
  <div class="mask-container" v-if="visible">
    <el-button class="close-button" :icon="Close" @click="handleClose" circle />
    <!-- <el-button class="close-button" @click="handleClose">close</el-button> -->
    <div class="swiper-container">
      <VideoSwiper :videoList="videoList" :isMask="true" :activeIdx="activeIdx"></VideoSwiper>
    </div>
  </div>
</template>

<style lang="less" scoped>
  .mask-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #00000087;
    overflow: hidden;

    .close-button {
      position: absolute;
      top: 50px;
      left: 50px;
      z-index: 100;
      width: 50px;
      height: 50px;
      font-size: 20px;
      color: #b9b9b9;
      background-color: #8f8eae87;
      border-color: #b9b9b9;
      &:hover {
        background-color: #b8bff387;
        color: #fff;
        border-color: #fff;
      }
    }
  }
</style>
