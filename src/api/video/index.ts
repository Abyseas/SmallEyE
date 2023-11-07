import type { BaseResponse } from '@/utils/request'
import { request } from '@/utils/request'
/**
 * @description 获取视频
 * @returns
 */
export function video(skip: number, limit: number = 20) {
  return request<BaseResponse<API.VideoResult>>({
    url: `database/videos?skip=${skip}&limit=${limit}`,
    method: 'get',
  })
}
// export function video() {
//   return request<BaseResponse<API.VideoResult>>({
//     url: 'videos',
//     method: 'get',
//   })
// }

export function videoCategory(category: string, skip: number, limit: number = 20) {
  return request<BaseResponse<API.VideoResult>>({
    url: `database/videos/category/${category}`,
    method: 'get',
  })
}
