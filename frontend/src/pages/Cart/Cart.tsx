import React from 'react'
import { Container } from './styles'
import { useCartContext } from '../../store/cartContext'

const Cart = () => {
  const { selectedPackage, order } = useCartContext()

  if (!selectedPackage || !order) {
    return <Container>No items in cart</Container>
  }

  return (
    <Container>
      <h2>Order Summary</h2>
      <p>
        Package: {selectedPackage.name} - €{selectedPackage.price}
      </p>
      <p>Recipient: {order.recipient_name}</p>
      <p>Mood: {order.mood}</p>
    </Container>
  )
}
export default Cart
