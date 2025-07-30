import React from 'react'
import { Container } from './styles'
import { useCartContext } from '../../store/cartContext'

const Cart = () => {
  const { selectedPackage, order } = useCartContext()

  if (!selectedPackage || !order) {
    return <Container>Your cart is empty.</Container>
  }

  return (
    <Container>
      <h2>Order Summary</h2>
      <p>
        <strong>Package:</strong> {selectedPackage.name} (€{selectedPackage.price})
      </p>
      <p>
        <strong>Recipient:</strong> {order.recipient_name}
      </p>
      <p>
        <strong>Mood:</strong> {order.mood}
      </p>
      {order.facts && (
        <p>
          <strong>Facts:</strong> {order.facts}
        </p>
      )}
    </Container>
  )
}

export default Cart
