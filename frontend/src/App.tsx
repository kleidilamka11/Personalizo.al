import React from 'react'
import AppRoutes from './routes/AppRoutes'
import MainLayout from './layouts/MainLayout'

const App = () => {
  return (
    <MainLayout>
      <AppRoutes />
    </MainLayout>
  )
}

export default App
