import React, { useState } from 'react'
import { Container } from './styles'
import Button from '../../components/Button'
import {
  register,
  requestVerification,
  verifyAccount,
} from '../../services/authService'

const Register = () => {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState('')
  const [registered, setRegistered] = useState(false)
  const [verified, setVerified] = useState(false)
  const [message, setMessage] = useState('')

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await register(email, username, password)
      const res = await requestVerification(email)
      setRegistered(true)
      setMessage(`Verification token: ${res.token}`)
    } catch (err) {
      setMessage('Registration failed')
    }
  }

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await verifyAccount(token)
      setVerified(true)
      setMessage('Account verified!')
    } catch (err) {
      setMessage('Verification failed')
    }
  }

  return (
    <Container>
      {!registered && (
        <form onSubmit={handleRegister}>
          <div>
            <input
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
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
          <Button label="Register" />
        </form>
      )}
      {registered && !verified && (
        <form onSubmit={handleVerify}>
          <p>{message}</p>
          <input
            placeholder="Verification token"
            value={token}
            onChange={(e) => setToken(e.target.value)}
          />
          <Button label="Verify" />
        </form>
      )}
      {verified && <p>{message}</p>}
    </Container>
  )
}
export default Register
