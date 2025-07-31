import React, { createContext, useContext, useState, useEffect } from 'react'
import {
  getAccessToken,
  getRefreshToken,
  clearTokens,
  saveTokens,
  isTokenExpired,
} from '../utils/token'
import { getMe, refreshToken as refreshTokenRequest } from '../services/authService'

type AuthContextType = {
  isAuthenticated: boolean
  setIsAuthenticated: (val: boolean) => void
  isAdmin: boolean
  setIsAdmin: (val: boolean) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => !!getAccessToken())
  const [isAdmin, setIsAdmin] = useState(false)

  const logout = () => {
    clearTokens()
    setIsAuthenticated(false)
    setIsAdmin(false)
  }

  useEffect(() => {
    if (process.env.NODE_ENV === 'test') return

    const init = async () => {
      let token = getAccessToken()
      const refresh = getRefreshToken()

      if (token && isTokenExpired(token)) {
        if (refresh) {
          try {
            const data = await refreshTokenRequest(refresh)
            saveTokens(data.access_token, data.refresh_token)
            token = data.access_token
          } catch {
            logout()
            return
          }
        } else {
          logout()
          return
        }
      }

      if (token) {
        try {
          const me = await getMe()
          setIsAuthenticated(true)
          setIsAdmin(me.is_admin)
        } catch {
          logout()
        }
      }
    }

    init()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])



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
