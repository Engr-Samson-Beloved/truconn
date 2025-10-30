"use client"

import * as React from 'react'
import { cn } from '@/lib/utils'
import { Shield, Wallet, Fingerprint, IdCard } from 'lucide-react'

export type DataCategory = 'Financial' | 'Biometric' | 'Health' | 'Identity'

const CATEGORIES: { key: DataCategory; title: string; description: string; icon: React.ElementType }[] = [
  { key: 'Financial', title: 'Financial', description: 'Bank details, transactions, credit history', icon: Wallet },
  { key: 'Biometric', title: 'Biometric', description: 'Fingerprint, facial recognition', icon: Fingerprint },
  { key: 'Health', title: 'Health', description: 'Medical records and history', icon: Shield },
  { key: 'Identity', title: 'Identity', description: 'NIN, passport, driver’s license', icon: IdCard as any },
]

interface DataCategorySelectorProps {
  value: DataCategory[]
  onChange: (value: DataCategory[]) => void
  className?: string
}

export function DataCategorySelector({ value, onChange, className }: DataCategorySelectorProps) {
  const toggle = (key: DataCategory) => {
    if (value.includes(key)) {
      onChange(value.filter((k) => k !== key))
    } else {
      onChange([...value, key])
    }
  }

  return (
    <div className={cn('grid grid-cols-1 md:grid-cols-2 gap-4', className)}>
      {CATEGORIES.map(({ key, title, description, icon: Icon }) => {
        const active = value.includes(key)
        return (
          <button
            type="button"
            key={key}
            onClick={() => toggle(key)}
            className={cn(
              'text-left p-4 rounded-lg border transition-all',
              active
                ? 'border-[#004C99] bg-[#004C990D]' // 5% blue
                : 'border-[#E0E4E8] hover:bg-[#F7F9FB]'
            )}
          >
            <div className="flex items-start gap-3">
              <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center', active ? 'bg-[#004C991A]' : 'bg-[#F0F2F5]')}>
                <Icon className={cn('w-5 h-5', active ? 'text-[#004C99]' : 'text-[#8B95A1]')} />
              </div>
              <div>
                <div className="font-semibold text-[#222222]">{title}</div>
                <div className="text-sm text-[#4A4A4A] mt-1">{description}</div>
              </div>
            </div>
          </button>
        )
      })}
    </div>
  )
}
