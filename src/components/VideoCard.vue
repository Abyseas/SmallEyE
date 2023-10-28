<script setup lang="ts">
  import IconHollowHeart from '~icons/custom/hollow_heart'
  const props = defineProps<{
    card_width: number
    video: API.VideoInfo
    muted: boolean
  }>()

  const emit = defineEmits(['mutedChange'])
  const video = ref()

  const playVideo = () => {
    video.value.currentTime = 0
    video.value.play()
    video.value.controls = true
  }

  const closeVideo = () => {
    video.value.pause()
    video.value.controls = false
    video.value.load()
  }

  const handleVolumeChange = (event: Event) => {
    emit('mutedChange', event)
  }
</script>
<template>
  <el-card class="video-card" :body-style="{ padding: '0px' }">
    <div class="video-cover" @mouseenter="playVideo" @mouseout="closeVideo">
      <!-- <el-image :src="props.video.thumb" fit="cover" /> -->
      <video
        class="video-content"
        type="video/mp4"
        :src="props.video.video_url"
        :poster="props.video.thumb"
        ref="video"
        :muted="props.muted"
        loop
        preload="auto"
        @volumechange="handleVolumeChange"
      ></video>
      <div class="like-container">
        <el-icon class="icon-box"><icon-hollow-heart></icon-hollow-heart></el-icon>
        <div>{{ props.video.like_num }}</div>
      </div>
    </div>

    <div class="video-card-footer">
      <div class="video-title"> {{ props.video.title }} </div>
      <div class="video-info"> @ {{ props.video.nickname }} - {{ props.video.mtime }}</div>
    </div>
  </el-card>
</template>

<style lang="less" scoped>
  @import '@/styles/video_card.less';
</style>
