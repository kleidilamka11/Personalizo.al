import axios from 'axios'
import {
  getAccessToken,
  getRefreshToken,
  saveTokens,
  clearTokens,
} from '../utils/token'
import { refreshToken as refreshTokenRequest } from './authService'

export const BACKEND_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BACKEND_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalConfig = error.config
    if (error.response?.status === 401 && !originalConfig._retry) {
      originalConfig._retry = true
      try {
        const refresh = getRefreshToken()
        if (!refresh) {
          clearTokens()
          return Promise.reject(error)
        }
        const data = await refreshTokenRequest(refresh)
        saveTokens(data.access_token, data.refresh_token)
        if (originalConfig.headers) {
          originalConfig.headers.Authorization = `Bearer ${data.access_token}`
        }
        return api(originalConfig)
      } catch (err) {
        clearTokens()
        return Promise.reject(err)
      }
    }
    return Promise.reject(error)
  },
)

export default api
