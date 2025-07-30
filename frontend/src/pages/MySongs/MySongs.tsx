import React, { useEffect, useState } from 'react'
import { Container } from './styles'
import { getMySongs } from '../../services/songService'
import { getOrders } from '../../services/orderService'
import { Song, Order } from '../../types/models'

const MySongs = () => {
  const [songs, setSongs] = useState<Song[]>([])
  const [orders, setOrders] = useState<Record<number, Order>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const songData = await getMySongs()
        setSongs(songData)
        const orderData = await getOrders()
        const map: Record<number, Order> = {}
        orderData.forEach((o: Order) => {
          map[o.id] = o
        })
        setOrders(map)
      } catch (err) {
        setError('Failed to load songs')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <Container>Loading...</Container>
  if (error) return <Container>{error}</Container>

  return (
    <Container>
      <h2>Your Songs</h2>
      {songs.length === 0 ? (
        <p>No songs found.</p>
      ) : (
        <ul>
          {songs.map((s) => (
            <li key={s.id} style={{ marginBottom: '1rem' }}>
              <p>Title: {s.title}</p>
              <p>Status: {orders[s.order_id]?.status || 'unknown'}</p>
              {orders[s.order_id]?.delivered_url && (
                <div>
                  <audio
                    data-testid="audio-player"
                    controls
                    src={orders[s.order_id].delivered_url || ''}
                  />
                  <a
                    data-testid="download-link"
                    href={orders[s.order_id].delivered_url || ''}
                    download
                  >
                    Download
                  </a>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </Container>
  )
}

export default MySongs
