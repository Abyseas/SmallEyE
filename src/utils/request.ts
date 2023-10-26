import axios from 'axios'
import type { AxiosRequestConfig } from 'axios'
const baseApiURL = 'https://www.fastmock.site/mock/974b3730b92341efc3b88c18c3490fc0/video'

const service = axios.create({
  baseURL: baseApiURL,
  timeout: 6000,
})

service.interceptors.response.use(
  (response) => {
    if (response.status === 200) {
      return Promise.resolve(response)
    } else {
      return Promise.reject(response)
    }
  },
  (error) => {
    return Promise.reject(error)
  },
)

export type Response<T = any> = {
  code: number
  message: string
  data: T
}

export type BaseResponse<T = any> = Promise<Response<T>>

/**
 *
 * @param method - request methods
 * @param url - request url
 * @param data - request data or params
 */
export const request = async <T = any>(config: AxiosRequestConfig): Promise<T> => {
  try {
    const res = await service.request(config)
    return res.data
  } catch (error: any) {
    return Promise.reject(error)
  }
}
