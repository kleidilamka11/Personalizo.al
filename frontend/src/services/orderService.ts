import api from './api'

export const getOrders = async () => {
  const response = await api.get('/orders/me')
  return response.data
}

export interface CreateOrderPayload {
  song_package_id: number
  recipient_name: string
  mood: string
  facts?: string
}

export const createOrder = async (payload: CreateOrderPayload) => {
  const response = await api.post('/orders/', payload)
  return response.data
}
