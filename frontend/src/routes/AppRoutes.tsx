import React from 'react'
import { Routes, Route } from 'react-router'
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

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/orders" element={<Orders />} />
      <Route path="/packages" element={<SongPackages />} />
      <Route path="/packages/:id" element={<PackageDetail />} />
      <Route path="/packages/:id/create" element={<SongForm />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/about" element={<About />} />
      <Route path="/mysongs" element={<MySongs />} />
    </Routes>
  )
}

export default AppRoutes
