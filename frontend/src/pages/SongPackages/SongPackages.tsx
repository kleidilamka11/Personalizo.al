import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Overlay, Modal, PackagesGrid, PackageCard } from './styles'

const packages = [
  {
    id: 'short',
    name: 'Short & Sweet',
    price: '€15',
    description: '30–45s song\n1 verse + hook',
  },
  {
    id: 'full',
    name: 'Full Package',
    price: '€29',
    description: '60–75s song\nCustom tone, extra detail',
  },
  {
    id: 'business',
    name: 'Business Ad',
    price: '€59–99',
    description: 'Commercial jingle\nCustom beat rights',
  },
]

const SongPackages = () => {
  const navigate = useNavigate()

  const handleSelect = (id: string) => {
    navigate(`/packages/${id}`)
  }

  return (
    <Overlay>
      <Modal>
        <h2>Select a Package</h2>
        <PackagesGrid>
          {packages.map((p) => (
            <PackageCard key={p.id} onClick={() => handleSelect(p.id)}>
              <h3>{p.name}</h3>
              <p>{p.price}</p>
              <small>{p.description}</small>
            </PackageCard>
          ))}
        </PackagesGrid>
      </Modal>
    </Overlay>
  )
}

export default SongPackages
