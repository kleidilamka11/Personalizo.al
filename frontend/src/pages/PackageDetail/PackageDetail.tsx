import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getPackage } from '../../services/songPackageService'
import { SongPackage } from '../../types/models'
import { Overlay, Modal, ActionButton } from './styles'

const PackageDetail = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [pack, setPack] = useState<SongPackage | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return
      try {
        const data = await getPackage(id)
        setPack(data)
      } catch {
        setPack(null)
      }
    }
    fetchData()
  }, [id])

  if (!pack) {
    return null
  }

  return (
    <Overlay>
      <Modal>
        <h2>{pack.name}</h2>
        <p>{pack.description}</p>
        <ActionButton onClick={() => navigate(`/packages/${id}/create`)}>
          Customize Song
        </ActionButton>
      </Modal>
    </Overlay>
  )
}

export default PackageDetail
