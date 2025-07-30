import React from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Overlay, Modal, ActionButton } from './styles'
import { useCartContext } from '../../store/cartContext'

const packages = {
  short: { id: 1, name: 'Short & Sweet', price: 15, desc: '30–45s song\n1 verse + hook' },
  full: { id: 2, name: 'Full Package', price: 29, desc: '60–75s song\nCustom tone, extra detail' },
  business: { id: 3, name: 'Business Ad', price: 59, desc: 'Commercial jingle\nCustom beat rights' },
}

const PackageDetail = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { setSelectedPackage } = useCartContext()
  const pack = id ? packages[id as keyof typeof packages] : undefined

  if (!pack) {
    return null
  }

  return (
    <Overlay>
      <Modal>
        <h2>{pack.name}</h2>
        <p>{pack.desc}</p>
        <ActionButton
          onClick={() => {
            setSelectedPackage({
              id: pack.id,
              name: pack.name,
              price: pack.price,
              description: pack.desc,
            })
            navigate(`/packages/${id}/create`)
          }}
        >
          Customize Song
        </ActionButton>
      </Modal>
    </Overlay>
  )
}

export default PackageDetail
