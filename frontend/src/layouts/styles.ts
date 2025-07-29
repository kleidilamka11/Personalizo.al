import styled from 'styled-components'

export const LayoutWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  height: 100%;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
  background: ${({ theme }) => theme.background};
  color: ${({ theme }) => theme.text};
`

export const MainContent = styled.main`
  flex: 1;
  display: flex; /* NEW */
  align-items: center; /* NEW: vertical centering */
  justify-content: center; /* NEW: horizontal centering */
  padding: 1.5rem;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;

  @media (min-width: 768px) {
    padding: 2rem;
  }
`

