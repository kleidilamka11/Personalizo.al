import React, { useState } from 'react'
import {
  AuthContainer,
  AuthCard,
  FormGroup,
  Input,
  GradientButton,
  Message,
} from '../../styles/authFormStyles'
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
    <AuthContainer>
      <AuthCard>
        {!registered && (
          <form onSubmit={handleRegister}>
            <FormGroup>
              <Input
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormGroup>
            <FormGroup>
              <Input
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
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
            <GradientButton type="submit">Register</GradientButton>
          </form>
        )}

        {registered && !verified && (
          <form onSubmit={handleVerify}>
            <Message>{message}</Message>
            <FormGroup>
              <Input
                placeholder="Verification token"
                value={token}
                onChange={(e) => setToken(e.target.value)}
              />
            </FormGroup>
            <GradientButton type="submit">Verify</GradientButton>
          </form>
        )}

        {verified && <Message>{message}</Message>}
      </AuthCard>
    </AuthContainer>
  )
}

export default Register
