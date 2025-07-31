import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthContext } from '../store/authContext'

interface Props {
  children: React.ReactElement
}

const AdminRoute: React.FC<Props> = ({ children }) => {
  const { isAuthenticated, isAdmin } = useAuthContext()
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return isAdmin ? children : <Navigate to="/" replace />
}

export default AdminRoute
