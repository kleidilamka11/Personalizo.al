export interface User {
  id: string
  email: string
  username: string
  isVerified: boolean
  is_admin?: boolean
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

export interface AdminOrder {
  id: number
  recipient_name: string
  mood: string | null
  facts: string | null
  status: string
  delivered_url?: string | null
  created_at: string
  user: {
    id: number
    email: string
  }
  package: {
    id: number
    name: string
  }
}
