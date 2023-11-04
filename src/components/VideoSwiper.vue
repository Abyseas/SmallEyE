<script setup lang="ts">
  import { Swiper, SwiperSlide } from 'swiper/vue'
  import { Navigation, Mousewheel, Keyboard } from 'swiper/modules'
  import IconComment from '~icons/custom/comment'
  import IconFilledHeart from '~icons/custom/filled_heart'
  // import IconMore from '~icons/custom/more'
  import IconStar from '~icons/custom/star'
  import IconPlus from '~icons/custom/plus'
  import IconShare from '~icons/custom/share'

  const props = defineProps<{
    videoList: API.VideoInfo[]
    isMask: boolean
    activeIdx: number
  }>()

  const muted = ref(true)

  const modules = [Navigation, Mousewheel, Keyboard]

  const handleMutedChange = (event: Event) => {
    const player = event.target as HTMLAudioElement
    muted.value = player.muted
  }

  const handleSlideChange = (swiper: any) => {
    const activeIndex = swiper.activeIndex
    props.videoList.forEach((_, s_index) => {
      const sPlayer = document.getElementById(`player${s_index}`) as HTMLAudioElement
      if (s_index !== activeIndex) {
        sPlayer.pause()
        sPlayer.controls = false
      } else {
        sPlayer.controls = true
        sPlayer.play()
      }
    })
  }
</script>

<template>
  <div class="video-swiper-container">
    <swiper
      ref="swiperRef"
      :class="props.isMask ? 'eye-swiper mask-swiper' : 'eye-swiper'"
      direction="vertical"
      :mousewheel="{
        thresholdTime: 1000,
      }"
      :parallax="true"
      :keyboard="true"
      :modules="modules"
      :initialSlide="props.activeIdx"
      @slideChange="handleSlideChange"
    >
      <swiper-slide v-for="(item, index) in videoList" :key="item.id">
        <div class="right_menus">
          <!-- 作者 -->
          <div class="menuClick">
            <el-tooltip effect="dark" content="进入作者主页" placement="right-start">
              <el-avatar :size="42" :src="item.avatar" />
            </el-tooltip>
            <el-tooltip effect="dark" content="关注" placement="right-start">
              <el-icon class="follow">
                <icon-plus></icon-plus>
              </el-icon>
            </el-tooltip>
          </div>
          <!-- 点赞 -->
          <div class="click-info">
            <el-tooltip effect="dark" content="点赞" placement="right-start">
              <el-icon>
                <icon-filled-heart></icon-filled-heart>
              </el-icon>
            </el-tooltip>
            <div class="text">{{ item.like_num }}</div>
          </div>
          <!-- 评论 -->
          <div class="click-info">
            <el-tooltip effect="dark" content="评论" placement="right-start">
              <el-icon>
                <icon-comment></icon-comment>
              </el-icon>
            </el-tooltip>
            <div class="text">{{ item.comment_num }}</div>
          </div>
          <!-- 收藏 -->
          <div class="click-info">
            <el-tooltip effect="dark" content="收藏" placement="right-start">
              <el-icon>
                <icon-star></icon-star>
              </el-icon>
            </el-tooltip>
            <div class="text">{{ item.collect_num }}</div>
          </div>
          <!-- 分享 -->
          <div class="click-info">
            <el-tooltip effect="dark" content="分享" placement="right-start">
              <el-icon>
                <icon-share></icon-share>
              </el-icon>
            </el-tooltip>
            <!-- <div class="text">{{ item.share_num }}</div> -->
          </div>
        </div>
        <div class="text-container">
          <div class="nickname"> @{{ item.nickname ? item.nickname : item.username }} </div>
          <div class="video-title">{{ item.title }}</div>
        </div>
        <video
          class="video-content"
          type="video/mp4"
          :id="`player${index}`"
          :src="item.video_url"
          :muted="muted"
          preload="auto"
          autoplay
          controls
          loop
          oncontextmenu="return false;"
          controlslist="nodownload noremoteplayback"
          :disablePictureInPicture="true"
          @volumechange="handleMutedChange"
        ></video>
      </swiper-slide>
    </swiper>
  </div>
</template>

<style lang="less" scoped>
  @import '@/styles/swiper.less';
</style>
