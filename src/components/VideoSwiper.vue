<script setup lang="ts">
  import { video } from '@/api/video'
  import { Swiper, SwiperSlide } from 'swiper/vue'
  import { Navigation, Mousewheel, Keyboard } from 'swiper/modules'
  import IconComment from '~icons/custom/comment'
  import IconHeart from '~icons/custom/heart'
  // import IconMore from '~icons/custom/more'
  import IconStar from '~icons/custom/star'
  import IconPlus from '~icons/custom/plus'
  import IconShare from '~icons/custom/share'
  const videoList = ref<API.VideoInfo[]>([])
  const muted = ref(true)
  const getVideoList = async () => {
    const videoResult = await video()
    videoList.value = videoResult.data.list
  }

  const modules = [Navigation, Mousewheel, Keyboard]

  getVideoList()

  const changeMuted = (event: any) => {
    const player = event.target as HTMLAudioElement
    muted.value = player.muted
  }

  const handleSlideChange = (swiper: any) => {
    const activeIndex = swiper.activeIndex
    const preIndex = swiper.previousIndex
    videoList.value.forEach((_, s_index) => {
      const sPlayer = document.getElementById(`player${s_index}`) as HTMLAudioElement
      if (s_index !== activeIndex) {
        sPlayer.pause()
        sPlayer.controls = false
      } else {
        sPlayer.addEventListener('volumechange', changeMuted)
        sPlayer.controls = true
        sPlayer.play()
      }

      if (s_index === preIndex) {
        sPlayer.removeEventListener('volumechange', changeMuted)
      }
    })
  }
</script>

<template>
  <div class="video-swiper-container" :style="`width: ${200}; height: ${200}`">
    <swiper
      ref="swiperRef"
      class="eye-swiper"
      direction="vertical"
      :mousewheel="{
        thresholdTime: 1000,
      }"
      :parallax="true"
      :keyboard="true"
      :modules="modules"
      @slideChange="handleSlideChange"
    >
      <swiper-slide v-for="(item, index) in videoList" :key="item.id">
        <div class="right_menus">
          <!-- 作者 -->
          <div class="menuClick">
            <el-tooltip effect="dark" content="进入作者主页" placement="right-start">
              <img class="avatar" :src="item.avatar" alt="" />
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
                <icon-heart></icon-heart>
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
          <div class="msg">{{ item.title }}</div>
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
          width="100%"
          height="100%"
          oncontextmenu="return false;"
          controlslist="nodownload noremoteplayback"
          :disablePictureInPicture="true"
        ></video>
      </swiper-slide>
    </swiper>
  </div>
</template>

<style lang="less" scoped>
  @import '@/styles/swiper.less';
</style>
