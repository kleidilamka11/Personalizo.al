import React, { useEffect, useState } from 'react'
import { Container } from './styles'
import {
  FormGroup,
  Input,
  GradientButton,
  Message,
} from '../../styles/authFormStyles'
import { getMe, updateMe, changePassword } from '../../services/authService'
import { User } from '../../types/models'

const Profile = () => {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data: User = await getMe()
        setEmail(data.email)
        setUsername(data.username)
      } catch (err) {
        setMessage('Failed to load profile')
      } finally {
        setLoading(false)
      }
    }
    fetchUser()
  }, [])

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await updateMe({ email, username })
      setMessage('Profile updated')
    } catch (err) {
      setMessage('Update failed')
    }
  }

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await changePassword(currentPassword, newPassword)
      setMessage('Password updated')
      setCurrentPassword('')
      setNewPassword('')
    } catch (err) {
      setMessage('Password change failed')
    }
  }

  if (loading) return <Container>Loading...</Container>

  return (
    <Container>
      <h2>Your Profile</h2>
      <form onSubmit={handleUpdate} style={{ marginBottom: '2rem' }}>
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
        <GradientButton type="submit">Update</GradientButton>
      </form>

      <form onSubmit={handlePasswordChange} style={{ marginBottom: '2rem' }}>
        <FormGroup>
          <Input
            type="password"
            placeholder="Current Password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
        </FormGroup>
        <FormGroup>
          <Input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </FormGroup>
        <GradientButton type="submit">Change Password</GradientButton>
      </form>

      {message && <Message>{message}</Message>}
    </Container>
  )
}

export default Profile
