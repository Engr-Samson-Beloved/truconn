"use client"

import * as React from 'react'

type Toast = { id: number; title?: string; description?: string }

const ToastContext = React.createContext<{
  toasts: Toast[]
  show: (t: Omit<Toast, 'id'>) => void
  remove: (id: number) => void
} | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<Toast[]>([])

  const show = (t: Omit<Toast, 'id'>) => setToasts((prev) => [...prev, { id: Date.now(), ...t }])
  const remove = (id: number) => setToasts((prev) => prev.filter((x) => x.id !== id))

  return (
    <ToastContext.Provider value={{ toasts, show, remove }}>
      {children}
      <div className="fixed bottom-4 right-4 space-y-2 z-50">
        {toasts.map((t) => (
          <div key={t.id} className="bg-white border border-[#E0E4E8] rounded-lg shadow px-4 py-3 min-w-[240px]">
            {t.title && <div className="font-semibold text-[#222222]">{t.title}</div>}
            {t.description && <div className="text-sm text-[#4A4A4A]">{t.description}</div>}
            <button className="text-xs text-[#004C99] mt-2" onClick={() => remove(t.id)}>Dismiss</button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = React.useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}
