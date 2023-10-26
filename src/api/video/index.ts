import type { BaseResponse } from '@/utils/request'
import { request } from '@/utils/request'

/**
 * @description 获取视频
 * @returns
 */
export function video() {
  return request<BaseResponse<API.VideoResult>>({
    url: 'hot',
    method: 'get',
  })
}
