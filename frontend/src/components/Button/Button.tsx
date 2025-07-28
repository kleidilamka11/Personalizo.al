import React from 'react'
import { StyledButton } from './styles'

type Props = {
  label: string
  onClick?: () => void
}

const Button: React.FC<Props> = ({ label, onClick }) => {
  return <StyledButton onClick={onClick}>{label}</StyledButton>
}

export default Button
