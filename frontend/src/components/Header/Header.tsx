import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthContext } from '../../store/authContext'
import { Container, Title, NavMenu, NavItem, LogoutButton } from './styles'

const Header = () => {
  const navigate = useNavigate()
  const { isAuthenticated, isAdmin, logout } = useAuthContext()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <Container>
      <Title>Personalizo.al</Title>
      <NavMenu>
        <NavItem to="/" end>
          Home
        </NavItem>
        <NavItem to="/packages">Package</NavItem>
        {isAuthenticated ? (
          <>
            {isAdmin && <NavItem to="/admin/orders">Admin</NavItem>}
            <NavItem to="/orders">Orders</NavItem>
            <NavItem to="/mysongs">My Songs</NavItem>
            <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
          </>
        ) : (
          <>
            <NavItem to="/about">About</NavItem>
            <NavItem to="/register">Register</NavItem>
            <NavItem to="/login">Login</NavItem>
          </>
        )}
      </NavMenu>
    </Container>
  )
}

export default Header
