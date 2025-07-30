import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
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

const SongForm = () => {
  const [mode, setMode] = useState<'simple' | 'custom'>('simple')
  const [instrumental, setInstrumental] = useState(false)
  const [isPublic, setIsPublic] = useState(true)
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    navigate('/cart')
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
          {mode === 'simple' ? (
            <TextArea placeholder="Tell us about the person" required />
          ) : (
            <>
              <Input placeholder="Song Title" required />
              <Input placeholder="Genre" />
              <Input placeholder="Mood" />
              <TextArea placeholder="Lyrics or details" />
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
