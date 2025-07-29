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
