import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthContext } from '../store/authContext'

interface Props {
  children: React.ReactElement
}

const ProtectedRoute: React.FC<Props> = ({ children }) => {
  const { isAuthenticated } = useAuthContext()
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return children
}

export default ProtectedRoute