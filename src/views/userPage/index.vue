<script setup lang="ts">
  import { h } from 'vue'
  import { ElDivider } from 'element-plus'
  const props = defineProps<{
    avatarSrc: string
    userInfo: {
      username: string
      like_num: string
      follow_num: string
      fans_num: string
    }
  }>()
  const emptySrc = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
  const emptyUserInfo = {
    username: '未登录',
    like_num: '-',
    follow_num: '-',
    fans_num: '-',
  }
  const spacer = h(ElDivider, {
    class: 'user-divider',
    direction: 'vertical',
    style: { borderLeft: '1px solid rgba(242,242,243, 0.1)' },
  })
</script>

<template>
  <div class="user-page-view">
    <div class="user-card">
      <el-avatar
        class="user-avatar"
        :size="120"
        :src="props.avatarSrc ? props.avatarSrc : emptySrc"
      ></el-avatar>
      <div class="user-info">
        <div class="username">{{ emptyUserInfo.username }}</div>
        <el-space :spacer="spacer">
          <div>
            <span>关注</span>
            <span class="number">{{ emptyUserInfo.like_num }}</span>
          </div>
          <div>
            <span>粉丝</span>
            <span class="number">{{ emptyUserInfo.follow_num }}</span>
          </div>
          <div>
            <span>获赞</span>
            <span class="number">{{ emptyUserInfo.fans_num }}</span>
          </div>
        </el-space>
      </div>
    </div>
    <el-tabs class="user-nav">
      <el-tab-pane name="productions" label="作品">作品</el-tab-pane>
      <el-tab-pane name="likes" label="喜欢">喜欢</el-tab-pane>
      <el-tab-pane name="collections" label="收藏">收藏</el-tab-pane>
      <el-tab-pane name="history" label="观看历史">观看历史</el-tab-pane>
    </el-tabs>
  </div>
</template>

<style lang="less">
  .user-page-view {
    background: linear-gradient(180deg, #243c61 0%, #8c96a7 100%);
    height: 100%;
    padding: 0 100px;

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
