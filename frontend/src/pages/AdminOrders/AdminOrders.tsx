import React, { useEffect, useState } from 'react'
import { Container } from './styles'
import { getAllOrders } from '../../services/adminService'
import { AdminOrder } from '../../types/models'

const AdminOrders = () => {
  const [orders, setOrders] = useState<AdminOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getAllOrders()
        setOrders(data)
      } catch (err) {
        setError('Failed to load orders')
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
      <h2>All Orders</h2>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <ul>
            {orders.map((o) => (
            <li key={o.id} style={{ marginBottom: '1rem' }}>
              <p>Order ID: {o.id}</p>
              <p>User: {o.user.email}</p>
              <p>Package: {o.package.name}</p>
              <p>Status: {o.status}</p>
            </li>
          ))}
        </ul>
      )}
    </Container>
  )
}

export default AdminOrders
