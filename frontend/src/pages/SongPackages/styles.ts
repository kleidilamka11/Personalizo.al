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
  text-align: center;
`

export const PackagesGrid = styled.div`
  margin-top: 1rem;
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;

  @media (min-width: 480px) {
    grid-template-columns: repeat(3, 1fr);
  }
`

export const PackageCard = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;

  h3 {
    margin: 0 0 0.25rem;
    font-size: 1rem;
  }

  p {
    margin: 0 0 0.25rem;
    font-weight: bold;
  }

  small {
    font-size: 0.8rem;
  }
`

export const CustomizeButton = styled.button`
  margin-top: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  background: ${({ theme }) => theme.primary};
  color: #fff;
  cursor: pointer;
`
