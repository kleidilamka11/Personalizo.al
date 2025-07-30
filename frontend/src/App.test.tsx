import React from 'react';
import { render, screen } from './testUtils';
import App from './App';

test('shows welcome text', () => {
  render(<App />);
  expect(screen.getByText(/Jari App is ready/i)).toBeInTheDocument();
});
