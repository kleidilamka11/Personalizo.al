import React from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Overlay, Modal, ActionButton } from './styles'

const packages = {
  short: { name: 'Short & Sweet', desc: '30–45s song\n1 verse + hook' },
  full: { name: 'Full Package', desc: '60–75s song\nCustom tone, extra detail' },
  business: { name: 'Business Ad', desc: 'Commercial jingle\nCustom beat rights' },
}

const PackageDetail = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const pack = id ? packages[id as keyof typeof packages] : undefined

  if (!pack) {
    return null
  }

  return (
    <Overlay>
      <Modal>
        <h2>{pack.name}</h2>
        <p>{pack.desc}</p>
        <ActionButton onClick={() => navigate(`/packages/${id}/create`)}>
          Customize Song
        </ActionButton>
      </Modal>
    </Overlay>
  )
}

export default PackageDetail
