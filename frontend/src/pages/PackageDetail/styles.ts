import styled from 'styled-components'

export const Overlay = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
`

export const Modal = styled.div`
  background: ${({ theme }) => theme.background};
  color: ${({ theme }) => theme.text};
  padding: 2rem 1.5rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  text-align: center;
`

export const ActionButton = styled.button`
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  background: ${({ theme }) => theme.primary};
  color: #fff;
  cursor: pointer;
`
