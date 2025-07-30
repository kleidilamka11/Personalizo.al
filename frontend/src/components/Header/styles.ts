import styled from 'styled-components'
import { NavLink } from 'react-router-dom'

export const Container = styled.header`
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
`

export const Title = styled.h1`
  font-size: 1.8rem;
  color: #222;
  margin: 0;
`

export const NavMenu = styled.nav`
  display: flex;
  gap: 1rem;
`

export const NavItem = styled(NavLink)`
  color: ${({ theme }) => theme.text};
  text-decoration: none;

  &.active {
    border-bottom: 2px solid ${({ theme }) => theme.primary};
  }
`

export const LogoutButton = styled.button`
  background: none;
  border: none;
  color: ${({ theme }) => theme.text};
  cursor: pointer;
`
