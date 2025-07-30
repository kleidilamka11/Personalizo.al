import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import { Overlay, Modal, ActionButton } from './styles'
import { getSongPackage } from '../../services/songPackageService'
import { SongPackage } from '../../types/models'
import { useCartContext } from '../../store/cartContext'

const PackageDetail = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { setPackage } = useCartContext()
  const [pack, setPack] = useState<SongPackage | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchPackage = async () => {
      try {
        if (id) {
          const data = await getSongPackage(Number(id))
          const mapped: SongPackage = {
            id: data.id,
            name: data.name,
            price: data.price_eur,
            description: data.description,
          }
          setPack(mapped)
        }
      } catch (err) {
        setError('Failed to load package')
      }
    }
    fetchPackage()
  }, [id])

  if (!pack) {
    return <Overlay>{error || 'Loading...'}</Overlay>
  }

  const handleCustomize = () => {
    setPackage(pack)
    navigate(`/packages/${id}/create`)
  }

  return (
    <Overlay>
      <Modal>
        <h2>{pack.name}</h2>
        <p>{pack.description}</p>
        <ActionButton onClick={handleCustomize}>Customize Song</ActionButton>
      </Modal>
    </Overlay>
  )
}

export default PackageDetail
