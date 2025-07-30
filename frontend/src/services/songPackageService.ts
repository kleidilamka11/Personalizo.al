import api from './api'
import { SongPackage } from '../types/models'

export const getPackage = async (id: number | string): Promise<SongPackage> => {
  const response = await api.get(`/packages/${id}`)
  return response.data
}

