import api from './api'

export const getSongPackages = async () => {
  const response = await api.get('/packages')
  return response.data
}
