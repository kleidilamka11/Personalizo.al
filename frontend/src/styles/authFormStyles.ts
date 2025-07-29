import styled from 'styled-components'

export const AuthContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* <- USE height not min-height here for full centering */
  padding: 1rem;
  background-color: ${({ theme }) => theme.background};
`



export const AuthCard = styled.div`
  background: rgba(255, 255, 255, 0.03);
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
`

export const FormGroup = styled.div`
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
`

export const Input = styled.input`
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 8px;
  background: ${({ theme }) => theme.inputBg};
  color: ${({ theme }) => theme.text};
  font-size: 1rem;

  &::placeholder {
    color: ${({ theme }) => theme.secondary};
  }
`

export const GradientButton = styled.button`
  width: 100%;
  padding: 0.9rem 1rem;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #ff4d4d, #9b00ff);
  color: #fff;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s;

  &:hover {
    opacity: 0.9;
  }
`

export const Message = styled.p`
  margin-top: 1rem;
  color: ${({ theme }) => theme.text};
  font-size: 0.9rem;
  text-align: center;
`
