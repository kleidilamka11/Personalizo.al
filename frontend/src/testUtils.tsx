import React from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { lightTheme } from './theme';
import { AuthProvider } from './store/authContext';

const AllProviders: React.FC<{children: React.ReactNode}> = ({ children }) => (
  <MemoryRouter>
    <AuthProvider>
      <ThemeProvider theme={lightTheme}>{children}</ThemeProvider>
    </AuthProvider>
  </MemoryRouter>
);

const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
