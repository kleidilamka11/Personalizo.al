import api from './api'

export const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password })
  return response.data
}

export const register = async (
  email: string,
  username: string,
  password: string
) => {
  const response = await api.post('/auth/register', {
    email,
    username,
    password,
  })
  return response.data
}

export const requestVerification = async (email: string) => {
  const response = await api.post('/auth/request-verify', { email })
  return response.data
}

export const verifyAccount = async (token: string) => {
  const response = await api.post('/auth/verify', { token })
  return response.data
}

export const getMe = async () => {
  const response = await api.get('/auth/me')
  return response.data
}

export interface UpdateUserPayload {
  email?: string
  username?: string
  password?: string
}

export const updateMe = async (payload: UpdateUserPayload) => {
  const response = await api.put('/auth/me', payload)
  return response.data
}

export const changePassword = async (
  currentPassword: string,
  newPassword: string,
) => {
  const response = await api.put('/auth/password', {
    current_password: currentPassword,
    new_password: newPassword,
  })
  return response.data
}

export const refreshToken = async (refreshToken: string) => {
  const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
  return response.data
}
