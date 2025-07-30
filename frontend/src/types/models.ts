export interface User {
  id: string
  email: string
  username: string
  isVerified: boolean
}

export interface SongPackage {
  id: number
  name: string
  price: number
  description: string
}

export interface Order {
  id: number
  song_package_id: number
  recipient_name: string
  mood: string
  facts?: string | null
  status: string
  delivered_url?: string | null
}

export interface Song {
  id: number
  order_id: number
  title: string
  genre: string
  duration_seconds?: number | null
  file_path: string
  created_at: string
}
