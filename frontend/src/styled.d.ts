import 'styled-components'

declare module 'styled-components' {
  export interface DefaultTheme {
    mode: 'light' | 'dark'
    background: string
    text: string
    inputBg: string
    primary: string
    secondary: string
  }
}
