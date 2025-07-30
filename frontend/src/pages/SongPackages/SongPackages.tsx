import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Overlay, Modal, PackagesGrid, PackageCard, CustomizeButton } from './styles'
import { useCartContext } from '../../store/cartContext'
import { SongPackage } from '../../types/models'

const packages: Array<SongPackage & { slug: string }> = [
  {
    id: 1,
    slug: 'short',
    name: 'Short & Sweet',
    price: 15,
    description: '30–45s song\n1 verse + hook',
  },
  {
    id: 2,
    slug: 'full',
    name: 'Full Package',
    price: 29,
    description: '60–75s song\nCustom tone, extra detail',
  },
  {
    id: 3,
    slug: 'business',
    name: 'Business Ad',
    price: 59,
    description: 'Commercial jingle\nCustom beat rights',
  },
]

const SongPackages = () => {
  const navigate = useNavigate()
  const { setSelectedPackage } = useCartContext()

  const handleCustomize = (pack: (typeof packages)[0]) => {
    setSelectedPackage({ id: pack.id, name: pack.name, price: pack.price, description: pack.description })
    navigate(`/packages/${pack.slug}/create`)
  }

  return (
    <Overlay>
      <Modal>
        <h2>Select a Package</h2>
        <PackagesGrid>
          {packages.map((p) => (
            <PackageCard key={p.id}>
              <h3>{p.name}</h3>
              <p>€{p.price}</p>
              <small>{p.description}</small>
              <CustomizeButton onClick={() => handleCustomize(p)}>
                Customize Song
              </CustomizeButton>
            </PackageCard>
          ))}
        </PackagesGrid>
      </Modal>
    </Overlay>
  )
}

export default SongPackages
