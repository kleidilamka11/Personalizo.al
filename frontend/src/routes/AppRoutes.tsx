import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from '../pages/Home'
import Login from '../pages/Login'
import Register from '../pages/Register'
import Orders from '../pages/Orders'
import SongPackages from '../pages/SongPackages'
import PackageDetail from '../pages/PackageDetail'
import SongForm from '../pages/SongForm'
import Cart from '../pages/Cart'
import Profile from '../pages/Profile'
import About from '../pages/About'
import MySongs from '../pages/MySongs'
import AdminOrders from '../pages/AdminOrders'
import AdminUpload from '../pages/AdminUpload'
import ProtectedRoute from './ProtectedRoute'
import AdminRoute from './AdminRoute'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/orders"
        element={
          <ProtectedRoute>
            <Orders />
          </ProtectedRoute>
        }
      />
      <Route path="/packages" element={<SongPackages />} />
      <Route path="/packages/:id" element={<PackageDetail />} />
      <Route
        path="/packages/:id/create"
        element={
          <ProtectedRoute>
            <SongForm />
          </ProtectedRoute>
        }
      />
      <Route
        path="/cart"
        element={
          <ProtectedRoute>
            <Cart />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />
      <Route path="/about" element={<About />} />
      <Route
        path="/mysongs"
        element={
          <ProtectedRoute>
            <MySongs />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/orders"
        element={
          <AdminRoute>
            <AdminOrders />
          </AdminRoute>
        }
      />
      <Route
        path="/admin/upload"
        element={
          <AdminRoute>
            <AdminUpload />
          </AdminRoute>
        }
      />
    </Routes>
  )
}

export default AppRoutes
