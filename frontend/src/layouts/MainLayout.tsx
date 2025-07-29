import React from 'react'
import Header from '../components/Header'
import Footer from '../components/Footer'
import { LayoutWrapper, MainContent } from './styles'

type Props = {
  children: React.ReactNode
}

const MainLayout: React.FC<Props> = ({ children }) => {
  return (
    <LayoutWrapper>
      <Header />
      <MainContent>{children}</MainContent>
      <Footer />
    </LayoutWrapper>
  )
}

export default MainLayout
