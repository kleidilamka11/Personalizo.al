import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from 'styled-components'
import { lightTheme, darkTheme } from './theme'

const Root = () => {
  const [isDarkMode, setIsDarkMode] = useState(true)

  return (
    <BrowserRouter>
      <ThemeProvider theme={isDarkMode ? darkTheme : lightTheme}>
        <App />
      </ThemeProvider>
    </BrowserRouter>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root')!)
root.render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>
)
