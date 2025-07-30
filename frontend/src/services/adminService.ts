import api from './api'

export const getAllOrders = async () => {
  const response = await api.get('/admin/orders/')
  return response.data
}

export interface UploadSongPayload {
  order_id: number
  title: string
  genre: string
  duration_seconds: number
  file: File
}

export const uploadSong = async (payload: UploadSongPayload) => {
  const data = new FormData()
  data.append('order_id', String(payload.order_id))
  data.append('title', payload.title)
  data.append('genre', payload.genre)
  data.append('duration_seconds', String(payload.duration_seconds))
  data.append('file', payload.file)
  const response = await api.post('/admin/songs/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}
