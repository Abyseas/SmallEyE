import { BaseResponse } from '@/utils/request'
import { request } from '@/utils/request'
/**
 * @description 用户注册
 * @returns
 */
export function register(user: API.UserInfo) {
  return request<BaseResponse<API.RegisterResult>>({
    url: `database/users/register`,
    method: 'post',
    data: user,
  })
}

/**
 * @description 用户登录
 * @returns
 */
export function login(user: API.UserInfo) {
  return request<BaseResponse<API.LoginResult>>({
    url: `login/token`,
    method: 'post',
    data: user,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}

export function userInfo() {
  return request<BaseResponse<API.UserInfoResult>>({
    url: `login/users/me`,
    method: 'get'
  })
}