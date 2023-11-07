export const skeletonList = [
  { id: 1 },
  { id: 2 },
  { id: 3 },
  { id: 4 },
  { id: 5 },
  { id: 6 },
  { id: 7 },
  { id: 8 },
  { id: 9 },
  { id: 10 },
  { id: 11 },
  { id: 12 },
]

const BASE_KEY = 'SMALLEYE_'

export const EXCEPTION_CODE_MESSAGE: { [key: number]: string } = {
  1001: '邮箱已被使用',
  1002: '用户不存在',
  1003: '用户名或密码不正确',
  1004: '无法验证凭证',
  1005: '用户未激活',
  1006: '没有验证',
  1007: '用户名已存在',
  1011: '视频不存在',
}

export const getExceptionMessage = (code: number) => {
  if (code in EXCEPTION_CODE_MESSAGE) {
    return EXCEPTION_CODE_MESSAGE[code]
  } else {
    return '未知错误'
  }
}

export type Token = {
  token_type: string
  access_token: string
}
export const storage = {
  set(key: string, value: any) {
    localStorage.setItem(BASE_KEY + key, JSON.stringify(value))
  },

  get<T>(key: string) {
    const value = localStorage.getItem(BASE_KEY + key)
    if (value && value !== undefined && value !== null) {
      return <T>JSON.parse(value)
    }
  },

  remove(key: string) {
    localStorage.removeItem(BASE_KEY + key)
  },
}
