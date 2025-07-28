import { useState, useEffect } from 'react'

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    // You can improve this with token checks later
    const token = localStorage.getItem('token')
    setIsAuthenticated(!!token)
  }, [])

  return { isAuthenticated }
}
