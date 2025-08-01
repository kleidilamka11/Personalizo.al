import api from './api'

export const createCheckout = async (orderId: number) => {
  const response = await api.post(`/payments/checkout/${orderId}`)
  return response.data
}
