"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { User } from "./api"
import { SessionManager } from "./session"

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (user: User) => void
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Load user from session on mount
    const savedUser = SessionManager.getUser()
    if (savedUser) {
      setUser(savedUser)
    }
    setIsLoading(false)
  }, [])

  const login = (userData: User) => {
    SessionManager.setUser(userData)
    setUser(userData)
  }

  const logout = () => {
    SessionManager.clearSession()
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        logout,
        isAuthenticated: user !== null,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

