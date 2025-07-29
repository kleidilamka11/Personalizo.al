import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ThemeProvider } from 'styled-components'
import { lightTheme, darkTheme } from './theme'
import { useState } from 'react'

const Root = () => {
  const [isDarkMode, setIsDarkMode] = useState(true)

  return (
    <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
      <App />
    </ThemeProvider>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root')!)
root.render(<Root />)
