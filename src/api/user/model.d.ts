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
    email?: string
    password: string
  } 

  type UserInfoResult = {
    username: string
    email: string
    id: number
    is_active: boolean
    follow_sum: 0,
    like_sum: 0,
    fans_sum: 0,
    videos: API.VideoInfo[]
  }

  type LoginResult = {
    accessToken: string,
    tokenType: string
  }
}

