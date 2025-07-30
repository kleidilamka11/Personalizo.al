import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import {
  Overlay,
  Modal,
  TabSwitcher,
  TabButton,
  Form,
  Input,
  TextArea,
  ToggleRow,
  SubmitButton,
} from './styles'
import { createOrder } from '../../services/orderService'
import { getSongPackage } from '../../services/songPackageService'
import { useCartContext } from '../../store/cartContext'
import { SongPackage } from '../../types/models'

const SongForm = () => {
  const [mode, setMode] = useState<'simple' | 'custom'>('simple')
  const [instrumental, setInstrumental] = useState(false)
  const [isPublic, setIsPublic] = useState(true)
  const [recipient, setRecipient] = useState('')
  const [mood, setMood] = useState('')
  const [facts, setFacts] = useState('')
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()
  const { setOrder, setPackage, selectedPackage } = useCartContext()
  const [pack, setPack] = useState<SongPackage | null>(selectedPackage)

  useEffect(() => {
    const fetchPackage = async () => {
      if (id && !pack) {
        const data = await getSongPackage(Number(id))
        const mapped: SongPackage = {
          id: data.id,
          name: data.name,
          price: data.price_eur,
          description: data.description,
        }
        setPack(mapped)
        setPackage(mapped)
      }
    }
    fetchPackage()
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!id) return
    try {
      const payload = {
        song_package_id: Number(id),
        recipient_name: recipient,
        mood,
        facts,
      }
      const data = await createOrder(payload)
      setOrder(data)
      navigate('/cart')
    } catch (err) {
      console.error('Failed to create order')
    }
  }

  return (
    <Overlay>
      <Modal>
        <TabSwitcher>
          <TabButton
            $active={mode === 'simple'}
            onClick={() => setMode('simple')}
          >
            Simple
          </TabButton>
          <TabButton
            $active={mode === 'custom'}
            onClick={() => setMode('custom')}
          >
            Custom
          </TabButton>
        </TabSwitcher>
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
          />
          {mode === 'simple' ? (
            <TextArea
              placeholder="Tell us about the person"
              value={facts}
              onChange={(e) => setFacts(e.target.value)}
              required
            />
          ) : (
            <>
              <Input placeholder="Song Title" required />
              <Input placeholder="Genre" />
              <TextArea
                placeholder="Lyrics or details"
                value={facts}
                onChange={(e) => setFacts(e.target.value)}
              />
            </>
          )}
          <ToggleRow>
            <label>
              <input
                type="checkbox"
                checked={instrumental}
                onChange={() => setInstrumental(!instrumental)}
              />{' '}
              Instrumental Mode
            </label>
            <label>
              <input
                type="checkbox"
                checked={isPublic}
                onChange={() => setIsPublic(!isPublic)}
              />{' '}
              Display Public
            </label>
          </ToggleRow>
          <SubmitButton type="submit">Generate Song</SubmitButton>
        </Form>
      </Modal>
    </Overlay>
  )
}

export default SongForm
