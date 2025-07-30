import React from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { ThemeProvider } from 'styled-components';
import { lightTheme } from './theme';
import { AuthProvider } from './store/authContext';
import { CartProvider } from './store/cartContext';

const AllProviders: React.FC<{children: React.ReactNode}> = ({ children }) => (
  <MemoryRouter>
    <AuthProvider>
      <CartProvider>
        <ThemeProvider theme={lightTheme}>{children}</ThemeProvider>
      </CartProvider>
    </AuthProvider>
  </MemoryRouter>
);

const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
