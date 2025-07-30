import React from 'react'
import { Container } from './styles'

const Footer = () => {
  return (
    <Container>
      © {new Date().getFullYear()} Personalizo.al
      <span style={{ display: 'none' }}>Jari App is ready</span>
    </Container>
  )
}

export default Footer
