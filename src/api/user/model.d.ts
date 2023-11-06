declare namespace API {
  type RegisterResult = {
    username: string
    email: string
    id: number
    is_active: boolean
    videos: API.VideoInfo[]
  }

  type UserInfo = {
    username: string
    email: string
    password: string
  }
}
