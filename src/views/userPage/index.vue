<script setup lang="ts">
  import { h } from 'vue'
  import { videoUsername, uploadVideo } from '@/api/video'
  import { UploadFilled } from '@element-plus/icons-vue'
  import { userInfo } from '@/api/user'
  import { ElDivider } from 'element-plus'
  import { cloneDeep } from 'lodash'
  import { ElMessage } from 'element-plus'
  import { Waterfall } from 'vue-waterfall-plugin-next'
  import SwiperMask from '@/components/SwiperMask.vue'
  import 'vue-waterfall-plugin-next/dist/style.css'
  import { getExceptionMessage } from '@/utils/common'
  import IconPlus from '~icons/custom/plus'
  import type { FormInstance } from 'element-plus'

  type userDetail = {
    username: string
    like_num: string | number
    follow_num: string | number
    fans_num: string | number
    avatar_url: string
    videoList: API.VideoInfo[]
  }

  const EMPTY_UPLOAD_INFO = {
    title: '',
    category: '',
    file: '',
  }

  const EMPTY_USER_INFO = {
    username: '未登录',
    like_num: '-',
    follow_num: '-',
    fans_num: '-',
    avatar_url: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    videoList: [],
  }

  const category_options = [
    {
      label: '生活',
      value: 'life',
    },
    {
      label: '资讯',
      value: 'news',
    },
    {
      label: '科技',
      value: 'tech',
    },
    {
      label: '知识',
      value: 'knowledge',
    },
    {
      label: '影视',
      value: 'movie',
    },
    {
      label: '时尚',
      value: 'fashion',
    },
    {
      label: '美食',
      value: 'food',
    },
    {
      label: '游戏',
      value: 'game',
    },
    {
      label: '音乐',
      value: 'music',
    },
    {
      label: '体育',
      value: 'sport',
    },
  ]

  const userDetails = ref<userDetail>(cloneDeep(EMPTY_USER_INFO))
  const spacer = h(ElDivider, {
    class: 'user-divider',
    direction: 'vertical',
    style: { borderLeft: '1px solid rgba(242,242,243, 0.1)' },
  })

  const getUserInfo = async () => {
    try {
      const userInfoResult = await userInfo()
      if (userInfoResult.code === 200) {
        userDetails.value.username = userInfoResult.data.username
        userDetails.value.like_num = userInfoResult.data.like_sum
        userDetails.value.follow_num = userInfoResult.data.follow_sum
        userDetails.value.fans_num = userInfoResult.data.fans_sum
        userDetails.value.videoList = userInfoResult.data.videos
      } else {
        ElMessage({
          message: getExceptionMessage(userInfoResult.code),
          type: 'error',
        })
      }
    } catch (error: any) {
      ElMessage({
        message: error.response.data.detail,
        type: 'error',
      })
    }
  }

  const videoListLen = ref(0)
  const visible = ref(false)
  const muted = ref(true)
  const activeIdx = ref(0)
  const showVideoSwiper = ref(false)
  const waterfallRef = ref()
  const uploadData = ref(cloneDeep(EMPTY_UPLOAD_INFO))
  const uploadFormRef = ref<InstanceType<typeof FormInstance>>()
  const uploadFile = ref()

  const uploadRules = {
    title: [{ required: true, message: '请输入视频标题', trigger: ['blur', 'change'] }],
    category: [{ required: true, message: '请选择视频类型', trigger: ['blur', 'change'] }],
    video: [{ required: true, message: '请上传视频', trigger: ['blur', 'change'] }],
  }

  const initVideoList = async () => {
    const videoResult = await videoUsername(userDetails.value.username, 0)
    userDetails.value.videoList = videoResult.data
    videoListLen.value = userDetails.value.videoList.length
  }

  const addVideoList = async (lastIdx: number) => {
    const videoResult = await videoUsername(userDetails.value.username, lastIdx)
    userDetails.value.videoList = userDetails.value.videoList.concat(videoResult.data)
    videoListLen.value = userDetails.value.videoList.length
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
  }, 100)

  const openUploadDialog = () => {
    visible.value = true
  }

  const closeDialog = () => {
    uploadData.value = cloneDeep(EMPTY_UPLOAD_INFO)
  }

  const changeFile = (file: any) => {
    uploadFile.value = file
  }

  const submitUpload = async (formEL: InstanceType<typeof FormInstance>) => {
    if (!formEL) return
    formEL.validate((valid: boolean) => {
      if (valid) {
      } else {
        ElMessage({
          message: '请确认信息输入无误',
          type: 'error',
        })
        return false
      }
    })
    uploadData.value.file = uploadFile.value.raw
    try {
      const uploadResult = await uploadVideo(uploadData.value)
      if (uploadResult.code === 200) {
        ElMessage({
          message: '登录成功',
          type: 'success',
        })
      } else {
        ElMessage({
          message: getExceptionMessage(uploadResult.code),
          type: 'error',
        })
      }
      console.log(uploadResult)
    } catch (error: any) {
      ElMessage({
        message: error.response.data.detail,
        type: 'error',
      })
    }
  }

  onMounted(() => {
    getUserInfo()
    setTimeout(() => {
      initVideoList()
    }, 300)
  })
</script>

<template>
  <div class="user-page-view">
    <div class="user-card">
      <el-avatar class="user-avatar" :size="120" :src="userDetails.avatar_url"></el-avatar>
      <div class="user-info">
        <div class="username">{{ userDetails.username }}</div>
        <el-space :spacer="spacer">
          <div>
            <span>关注</span>
            <span class="number">{{ userDetails.like_num }}</span>
          </div>
          <div>
            <span>粉丝</span>
            <span class="number">{{ userDetails.follow_num }}</span>
          </div>
          <div>
            <span>获赞</span>
            <span class="number">{{ userDetails.fans_num }}</span>
          </div>
        </el-space>
      </div>
      <div class="plus-icon-container" @click="openUploadDialog">
        <el-icon size="100" style="margin: auto"> <IconPlus></IconPlus></el-icon>
      </div>
      <el-dialog class="upload" v-model="visible" @close="closeDialog" raw="">
        <el-card class="form-container">
          <el-form :model="uploadData" :rules="uploadRules" ref="uploadFormRef" status-icon>
            <el-form-item class="upload-form-item" prop="title">
              <el-input v-model="uploadData.title" placeholder="视频标题"> </el-input>
            </el-form-item>
            <el-form-item class="upload-form-item" prop="category">
              <el-select v-model="uploadData.category" placeholder="视频类型" clearable>
                <el-option
                  v-for="item in category_options"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-upload drag :data="uploadData" :on-change="changeFile">
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text"> 拖拽文件上传 或者 <em>点击上传</em> </div>
                <template #tip>
                  <div class="el-upload__tip"> video files </div>
                </template>
              </el-upload>
            </el-form-item>
          </el-form>
          <el-button class="base-button" @click="submitUpload(uploadFormRef)">上传</el-button>
        </el-card>
      </el-dialog>
    </div>
    <el-tabs class="user-nav">
      <el-tab-pane name="productions" label="作品">
        <div
          class="pane-container"
          v-infinite-scroll="
            () => {
              addVideoList(videoListLen)
            }
          "
          :infinite-scroll-immediate="false"
        >
          <Waterfall :list="userDetails.videoList" :width="300" ref="waterfallRef">
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
            :videoList="userDetails.videoList"
            :visible="showVideoSwiper"
            :activeIdx="activeIdx"
            @closeVideoMask="handleCloseVideoMask"
            @reachEnd="handleReachEnd"
          ></SwiperMask>
        </div>
      </el-tab-pane>
      <el-tab-pane name="likes" label="喜欢">待完善</el-tab-pane>
      <el-tab-pane name="collections" label="收藏">待完善</el-tab-pane>
      <el-tab-pane name="history" label="观看历史">待完善</el-tab-pane>
    </el-tabs>
  </div>
</template>

<style lang="less">
  @import '@/styles/variables.less';
  .user-page-view {
    background: linear-gradient(180deg, #243c61 0%, #8c96a7 100%);
    height: calc(100vh - @header-height);
    padding: 0 100px;
    overflow: hidden;

    .el-dialog.upload {
      // background: #AEBDDB;
      background-image: url('../../assets/background3.png');
      background-size: cover;
      border-radius: 15px;
      max-width: 600px;
      height: 50%;
      width: 50%;
      text-align: center;
      .el-dialog__headerbtn:hover .el-dialog__close {
        color: #fff;
      }

      .el-form-item__content {
        display: block;
      }
      .el-dialog__headerbtn:focus .el-dialog__close {
        color: #fff;
      }
      .el-dialog__close {
        color: @theme-color;
      }

      .form-container {
        border-radius: 15px;
        margin-top: 20px;
        margin: 20px;
        .form-icon {
          color: #777;
          font-size: 20px;
        }

        .el-input {
          height: 45px;
        }
        .el-input__wrapper.is-focus {
          box-shadow: 0 0 0 1px #7697da inset;
        }
      }

      .upload-form-item {
        margin-left: 20px;
        margin-right: 20px;
      }

      .check-button {
        font-size: 12px;
      }

      .bottom-button {
        width: 100px;
      }
    }

    .plus-icon-container {
      margin-right: 300px;
      background-color: rgb(200, 203, 208);
      text-align: center;
      border-radius: 5px;
      display: flex;

      &:hover {
        background-color: #fff;
        cursor: pointer;
      }
    }

    .pane-container {
      height: 100%;
      overflow-y: auto;
    }
    .waterfall-list {
      background-color: transparent !important;
    }

    .user-card {
      color: #a0a2bc;
      margin-bottom: 50px;
      display: flex;
      .user-info {
        margin: auto;
        margin-left: 50px;
      }

      .username {
        font-size: 20px;
        font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
        color: #fff;
        margin-bottom: 20px;
      }
      .number {
        color: #fff;
        margin-left: 5px;
        font-size: 12px;
      }
    }

    .user-nav {
      .el-tabs__item {
        color: #a0a2bc;
        font-size: 20px;
        height: 80px;
      }

      .el-tabs__item.is-active {
        color: #fff;
      }

      .el-tabs__nav-wrap::after {
        height: 1px;
        background-color: rgba(256, 256, 256, 0.1);
      }

      .el-tabs__active-bar {
        background-color: #fff;
      }
    }
  }
</style>
