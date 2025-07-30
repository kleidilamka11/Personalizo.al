// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import { BrowserRouter } from "react-router";


// The test environment does not install real browser routing or HTTP libraries.
// Provide lightweight mocks so components depending on these packages can load.
jest.mock('react-router', () => {
  const React = require('react');
  return {
    MemoryRouter: ({ children }: { children: React.ReactNode }) => (
      <div>{children}</div>
    ),
    BrowserRouter: ({ children }: { children: React.ReactNode }) => (
      <div>{children}</div>
    ),
    Routes: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    Route: ({ element }: { element: React.ReactNode }) => <>{element}</>,
    NavLink: ({ to, children }: { to: string; children: React.ReactNode }) => (
      <a href={to}>{children}</a>
    ),
    Link: ({ to, children }: { to: string; children: React.ReactNode }) => (
      <a href={to}>{children}</a>
    ),
    useNavigate: () => jest.fn(),
    useParams: () => ({}),
  };
});

jest.mock('axios', () => {
  return {
    create: () => ({
      interceptors: { request: { use: jest.fn() } },
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
    }),
  };
});
