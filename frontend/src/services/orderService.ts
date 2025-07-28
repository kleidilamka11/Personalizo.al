import api from './api'

export const getOrders = async () => {
  const response = await api.get('/orders/me')
  return response.data
}
