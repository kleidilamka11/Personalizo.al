import React, { createContext, useContext, useState } from 'react'
import { SongPackage, Order } from '../types/models'

interface CartContextType {
  selectedPackage: SongPackage | null
  order: Order | null
  setPackage: (p: SongPackage | null) => void
  setOrder: (o: Order | null) => void
  clearCart: () => void
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedPackage, setSelectedPackage] = useState<SongPackage | null>(null)
  const [order, setOrder] = useState<Order | null>(null)

  const clearCart = () => {
    setSelectedPackage(null)
    setOrder(null)
  }

  return (
    <CartContext.Provider
      value={{ selectedPackage, order, setPackage: setSelectedPackage, setOrder, clearCart }}
    >
      {children}
    </CartContext.Provider>
  )
}

export const useCartContext = () => {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCartContext must be used within CartProvider')
  return ctx
}
