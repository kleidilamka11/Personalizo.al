import React from 'react'
import { Container, Title, NavMenu, NavItem } from './styles'

const Header = () => {
  return (
    <Container>
      <Title>Personalizo.al</Title>
      <NavMenu>
        <NavItem to="/" end>
          Home
        </NavItem>
        <NavItem to="/packages">Packages</NavItem>
        <NavItem to="/orders">Orders</NavItem>
        <NavItem to="/profile">Profile</NavItem>
        <NavItem to="/login">Login</NavItem>
        <NavItem to="/register">Register</NavItem>
      </NavMenu>
    </Container>
  )
}

export default Header
