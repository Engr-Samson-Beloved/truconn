"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { User } from "./api"
import { SessionManager } from "./session"
import { AuthAPI } from "./api"

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
    const loadUser = () => {
      const savedUser = SessionManager.getUser()
      if (savedUser) {
        setUser(savedUser)
      } else {
        setUser(null)
      }
      setIsLoading(false)
    }
    loadUser()

    // Listen for storage changes (e.g., when another tab logs out)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "truconn_user" || e.key === null) {
        const savedUser = SessionManager.getUser()
        if (savedUser) {
          setUser(savedUser)
        } else {
          setUser(null)
        }
      }
    }

    if (typeof window !== "undefined") {
      window.addEventListener('storage', handleStorageChange)
      return () => window.removeEventListener('storage', handleStorageChange)
    }
  }, [])

  const login = (userData: User) => {
    // Clear any previous session data first to prevent session mixing
    SessionManager.clearSession()
    // Set new user data
    SessionManager.setUser(userData)
    setUser(userData)
  }

  const logout = async () => {
    try {
      // Call backend logout API to clear server session
      await AuthAPI.logout()
    } catch (error) {
      // Continue with local logout even if backend call fails
      console.error("Logout API call failed:", error)
    } finally {
      // Always clear local session
      SessionManager.clearSession()
      setUser(null)
    }
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

