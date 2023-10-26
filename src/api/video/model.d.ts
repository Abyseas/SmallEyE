declare namespace API {
  type VideoInfo = {
    id: number
    avatar: string
    username: string
    nickname: string
    user_id: number
    is_follow: number
    title: string
    thumb: string
    video_url: string
    mtime: string
    like_num: number
    collect_num: number
    comment_num: number
    share_num: number
  }
  /** 登录成功结果 */
  type VideoResult = {
    total: number
    total_page: number
    current_page: number
    list: VideoInfo[]
  }
}
