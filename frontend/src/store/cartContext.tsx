import React, { createContext, useContext, useState } from 'react'
import { SongPackage, Order } from '../types/models'

type CartContextType = {
  selectedPackage: SongPackage | null
  setSelectedPackage: (p: SongPackage | null) => void
  order: Order | null
  setOrder: (o: Order | null) => void
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [selectedPackage, setSelectedPackage] = useState<SongPackage | null>(null)
  const [order, setOrder] = useState<Order | null>(null)

  return (
    <CartContext.Provider value={{ selectedPackage, setSelectedPackage, order, setOrder }}>
      {children}
    </CartContext.Provider>
  )
}

export const useCartContext = () => {
  const context = useContext(CartContext)
  if (!context) throw new Error('useCartContext must be used within CartProvider')
  return context
}
