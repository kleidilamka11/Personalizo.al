import api from './api'

export const getSongPackages = async () => {
  const response = await api.get('/packages')
  return response.data
}

export const getSongPackage = async (id: number) => {
  const response = await api.get(`/packages/${id}`)
  return response.data
}
