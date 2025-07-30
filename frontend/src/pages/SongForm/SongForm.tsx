import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCartContext } from '../../store/cartContext'
import { createOrder } from '../../services/orderService'
import { Overlay, Modal, Form, Input, TextArea, SubmitButton } from './styles'

const SongForm = () => {
  const [recipient, setRecipient] = useState('')
  const [mood, setMood] = useState('')
  const [facts, setFacts] = useState('')
  const navigate = useNavigate()
  const { selectedPackage, setOrder } = useCartContext()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedPackage) return
    try {
      const order = await createOrder({
        song_package_id: selectedPackage.id,
        recipient_name: recipient,
        mood,
        facts,
      })
      setOrder(order)
      navigate('/cart')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <Overlay>
      <Modal>
        <h2>Create your song</h2>
        <Form onSubmit={handleSubmit}>
          <Input
            placeholder="Recipient Name"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
          />
          <Input
            placeholder="Mood"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            required
          />
          <TextArea
            placeholder="Facts about them"
            value={facts}
            onChange={(e) => setFacts(e.target.value)}
          />
          <SubmitButton type="submit">Submit Order</SubmitButton>
        </Form>
      </Modal>
    </Overlay>
  )
}

export default SongForm
