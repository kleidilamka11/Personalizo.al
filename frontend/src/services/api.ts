import axios from 'axios'
import { getToken } from '../utils/token'

export const BACKEND_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BACKEND_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
