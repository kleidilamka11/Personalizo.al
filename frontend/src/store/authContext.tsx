import React, { createContext, useContext, useState } from 'react'
import { getToken, clearToken } from '../utils/token'

type AuthContextType = {
  isAuthenticated: boolean
  setIsAuthenticated: (val: boolean) => void
  isAdmin: boolean
  setIsAdmin: (val: boolean) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => !!getToken())
  const [isAdmin, setIsAdmin] = useState(false)

  const logout = () => {
    clearToken()
    setIsAuthenticated(false)
    setIsAdmin(false)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, isAdmin, setIsAdmin, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuthContext = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuthContext must be used within AuthProvider')
  return context
}
