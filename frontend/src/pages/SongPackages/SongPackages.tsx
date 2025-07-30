import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import { Overlay, Modal, PackagesGrid, PackageCard } from './styles'
import { getSongPackages } from '../../services/songPackageService'
import { SongPackage } from '../../types/models'
import { useCartContext } from '../../store/cartContext'

const SongPackages = () => {
  const [packages, setPackages] = useState<SongPackage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { setPackage } = useCartContext()

  useEffect(() => {
    const fetchPackages = async () => {
      try {
        const data = await getSongPackages()
        const mapped = data.map((p: any) => ({
          id: p.id,
          name: p.name,
          price: p.price_eur,
          description: p.description,
        }))
        setPackages(mapped)
      } catch (err) {
        setError('Failed to load packages')
      } finally {
        setLoading(false)
      }
    }
    fetchPackages()
  }, [])

  const handleSelect = (id: number) => {
    setPackage(null)
    navigate(`/packages/${id}`)
  }

  return (
    <Overlay>
      <Modal>
        <h2>Select a Package</h2>
        {loading && <p>Loading...</p>}
        {error && <p>{error}</p>}
        <PackagesGrid>
          {packages.map((p) => (
            <PackageCard key={p.id} onClick={() => handleSelect(p.id)}>
              <h3>{p.name}</h3>
              <p>€{p.price}</p>
              <small>{p.description}</small>
            </PackageCard>
          ))}
        </PackagesGrid>
      </Modal>
    </Overlay>
  )
}

export default SongPackages
