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
  max-width: 500px;
`

export const TabSwitcher = styled.div`
  display: flex;
  margin-bottom: 1rem;
`

export const TabButton = styled.button<{ $active: boolean }>`
  flex: 1;
  padding: 0.5rem;
  border: none;
  background: ${({ $active, theme }) =>
    $active ? theme.primary : 'transparent'};
  color: ${({ $active, theme }) => ($active ? '#fff' : theme.text)};
  cursor: pointer;
`

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`

export const Input = styled.input`
  padding: 0.6rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #444;
  background: ${({ theme }) => theme.inputBg};
  color: ${({ theme }) => theme.text};
`

export const TextArea = styled.textarea`
  padding: 0.6rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #444;
  background: ${({ theme }) => theme.inputBg};
  color: ${({ theme }) => theme.text};
  min-height: 80px;
`

export const ToggleRow = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
`

export const SubmitButton = styled.button`
  margin-top: 0.5rem;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  background: ${({ theme }) => theme.primary};
  color: #fff;
  cursor: pointer;
`
