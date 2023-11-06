import type { BaseResponse } from '@/utils/request'
import { request } from '@/utils/request'
/**
 * @description 获取视频
 * @returns
 */
export function register(user: API.UserInfo) {
  return request<BaseResponse<API.RegisterResult>>({
    url: `users/register`,
    method: 'post',
    data: user,
  })
}
