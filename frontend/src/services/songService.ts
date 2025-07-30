import api from './api'

export const getMySongs = async () => {
  const response = await api.get('/songs/me')
  return response.data
}

export const getSongByOrder = async (orderId: number) => {
  const response = await api.get(`/songs/${orderId}`)
  return response.data
}
