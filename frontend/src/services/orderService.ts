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

export interface UpdateOrderPayload {
  recipient_name?: string
  mood?: string
  facts?: string
}

export const updateOrder = async (id: number, payload: UpdateOrderPayload) => {
  const response = await api.patch(`/orders/${id}`, payload)
  return response.data
}

export interface CancelOrderPayload {
  reason?: string
}

export const cancelOrder = async (
  id: number,
  payload?: CancelOrderPayload,
) => {
  const response = await api.post(`/orders/${id}/cancel`, payload)
  return response.data
}
