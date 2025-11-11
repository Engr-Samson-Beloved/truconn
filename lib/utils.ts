import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Get CSRF token from cookies
 * Django sets the CSRF token in a cookie named 'csrftoken'
 */
export function getCsrfToken(): string | null {
  if (typeof document === 'undefined') return null
  
  const cookies = document.cookie.split(';')
  const csrfCookie = cookies.find((c) => c.trim().startsWith('csrftoken='))
  
  if (csrfCookie) {
    return decodeURIComponent(csrfCookie.split('=')[1])
  }
  
  return null
}

/**
 * Get default headers for API requests
 * Includes CSRF token if available
 */
export function getApiHeaders(): HeadersInit {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  
  // Prefer CSRF from cookie; fallback to localStorage (persisted after login)
  let csrfToken = getCsrfToken()
  if (!csrfToken && typeof window !== 'undefined') {
    try {
      const stored = window.localStorage.getItem('truconn_token')
      if (stored) csrfToken = stored
    } catch {
      // ignore storage errors
    }
  }
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }
  
  return headers
}