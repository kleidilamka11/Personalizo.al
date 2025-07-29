import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Container } from './styles'
import Button from '../../components/Button'
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
    <Container>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button label="Login" />
      </form>
      {message && <p>{message}</p>}
    </Container>
  )
}

export default Login
