import React, { useState } from 'react'
import { Container } from './styles'
import { uploadSong } from '../../services/adminService'

const AdminUpload = () => {
  const [orderId, setOrderId] = useState('')
  const [title, setTitle] = useState('')
  const [genre, setGenre] = useState('')
  const [duration, setDuration] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    try {
      await uploadSong({
        order_id: Number(orderId),
        title,
        genre,
        duration_seconds: Number(duration),
        file,
      })
      setMessage('Song uploaded')
    } catch (err) {
      setMessage('Upload failed')
    }
  }

  return (
    <Container>
      <h2>Upload Song</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Order ID"
          value={orderId}
          onChange={(e) => setOrderId(e.target.value)}
        />
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          placeholder="Genre"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        />
        <input
          placeholder="Duration seconds"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
        />
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
    </Container>
  )
}

export default AdminUpload
