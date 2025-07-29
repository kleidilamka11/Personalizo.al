import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  AuthContainer,
  AuthCard,
  FormGroup,
  Input,
  GradientButton,
  Message,
} from '../../styles/authFormStyles'
import { login } from '../../services/authService'
import { saveToken } from '../../utils/token'
import { useAuthContext } from '../../store/authContext'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const navigate = useNavigate()
  const { setIsAuthenticated } = useAuthContext()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const data = await login(email, password)
      saveToken(data.access_token)
      setIsAuthenticated(true)
      navigate('/')
    } catch (err) {
      setMessage('Login failed')
    }
  }

  return (
    <AuthContainer>
      <AuthCard>
        <form onSubmit={handleSubmit}>
          <FormGroup>
            <Input
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </FormGroup>
          <FormGroup>
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </FormGroup>
          <GradientButton type="submit">Login</GradientButton>
        </form>
        {message && <Message>{message}</Message>}
      </AuthCard>
    </AuthContainer>
  )
}

export default Login
