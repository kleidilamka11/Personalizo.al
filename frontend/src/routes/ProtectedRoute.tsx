import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthContext } from '../store/authContext'

interface Props {
  children: React.JSX.Element
}

const ProtectedRoute: React.FC<Props> = ({ children }) => {
  const { isAuthenticated } = useAuthContext()
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

export default ProtectedRoute
