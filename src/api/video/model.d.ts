declare namespace API {
  type VideoInfo = {
    id: number
    owner_id: number
    author: string
    title: string
    category: string
    avatar_url: string
    cover_url: string
    video_url: string
    like_count: number
    collect_count: number
    comment_count: number
    share_count: number
    create_time: string
  }
  /** 登录成功结果 */
  type VideoResult = VideoInfo[]
}
