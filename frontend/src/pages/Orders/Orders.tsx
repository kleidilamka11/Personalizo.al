import React, { useEffect, useState } from 'react'
import { Container } from './styles'
import { getOrders, cancelOrder } from '../../services/orderService'
import { getSongPackages } from '../../services/songPackageService'
import { Order, SongPackage } from '../../types/models'

const Orders = () => {
  const [orders, setOrders] = useState<Order[]>([])
  const [packages, setPackages] = useState<Record<number, SongPackage>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const orderData = await getOrders()
        setOrders(orderData)
        const pkgData = await getSongPackages()
        const map: Record<number, SongPackage> = {}
        pkgData.forEach((p: any) => {
          map[p.id] = {
            id: p.id,
            name: p.name,
            price: p.price_eur,
            description: p.description,
          }
        })
        setPackages(map)
      } catch (err) {
        setError('Failed to load orders')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const handleCancel = async (id: number) => {
    try {
      const updated = await cancelOrder(id)
      setOrders((prev) =>
        prev.map((o) => (o.id === id ? { ...o, status: updated.status } : o)),
      )
    } catch (err) {
      console.error('Failed to cancel order')
    }
  }

  if (loading) return <Container>Loading...</Container>
  if (error) return <Container>{error}</Container>

  return (
    <Container>
      <h2>Your Orders</h2>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <ul>
          {orders.map((o) => (
              <li key={o.id} style={{ marginBottom: '1rem' }}>
                <p>
                  Package:{' '}
                  {packages[o.song_package_id]?.name || o.song_package_id}
                </p>
                <p>Status: {o.status}</p>
                {o.status === 'pending' && (
                  <button onClick={() => handleCancel(o.id)}>Cancel</button>
                )}
                {o.delivered_url && (
                  <div>
                    <audio
                      data-testid="audio-player"
                      controls
                      src={o.delivered_url}
                    />
                    <a
                      data-testid="download-link"
                      href={o.delivered_url}
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

export default Orders
