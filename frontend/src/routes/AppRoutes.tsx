import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from '../pages/Home'
import Login from '../pages/Login'
import Register from '../pages/Register'
import Orders from '../pages/Orders'
import SongPackages from '../pages/SongPackages'
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
      <Route path="/profile" element={<Profile />} />
      <Route path="/about" element={<About />} />
      <Route path="/mysongs" element={<MySongs />} />
    </Routes>
  )
}

export default AppRoutes
