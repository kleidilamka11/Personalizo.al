import React from 'react'
import { Container } from './styles'
import { useCartContext } from '../../store/cartContext'
import { createCheckout } from '../../services/paymentService'

const Cart = () => {
  const { selectedPackage, order } = useCartContext()

  if (!selectedPackage || !order) {
    return <Container>No items in cart</Container>
  }

  const handlePay = async () => {
    try {
      const data = await createCheckout(order.id)
      window.location.href = data.url
    } catch (err) {
      console.error('Failed to initiate payment')
    }
  }

  return (
    <Container>
      <h2>Order Summary</h2>
      <p>
        Package: {selectedPackage.name} - €{selectedPackage.price}
      </p>
      <p>Recipient: {order.recipient_name}</p>
      <p>Mood: {order.mood}</p>
      <button onClick={handlePay}>Pay Now</button>
    </Container>
  )
}
export default Cart
