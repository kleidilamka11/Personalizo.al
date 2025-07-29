import styled from 'styled-components'

export const LayoutWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
  background: ${({ theme }) => theme.background};
  color: ${({ theme }) => theme.text};
`

export const MainContent = styled.main`
  flex: 1;
  padding: 1.5rem;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;

  @media (min-width: 768px) {
    padding: 2rem;
  }
`
