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

export function hotVideo(skip: number, limit: number = 20) {
  return request<BaseResponse<API.VideoResult>>({
    url: `database/videos?skip=${skip}&limit=${limit}&is_recommend=true`,
    method: 'get',
  })
}

export function videoCategory(category: string, skip: number, limit: number = 20) {
  return request<BaseResponse<API.VideoResult>>({
    url: `database/videos/category/${category}?skip=${skip}&limit=${limit}`,
    method: 'get',
  })
}

export function videoUsername(username: string, skip: number, limit: number = 20) {
  return request<BaseResponse<API.VideoResult>>({
    url: `database/videos/user/${username}?skip=${skip}&limit=${limit}`,
    method: 'get',
  })
}

export function uploadVideo(data: any) {
  return request<BaseResponse<API.VideoInfo>>({
    url: `login/videos/me/upload`,
    method: 'post',
    data: data,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
}
