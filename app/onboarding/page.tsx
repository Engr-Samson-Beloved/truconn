"use client"

import { OnboardingStepper } from '@/components/onboarding-stepper'
import { useRouter } from 'next/navigation'

export default function OnboardingPage() {
  const router = useRouter()
  return (
    <div className="min-h-screen" style={{ background: '#F7F9FB' }}>
      <div className="max-w-4xl mx-auto px-4 py-10">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ background: '#004C99' }}>
            <span className="text-white font-bold">✓</span>
          </div>
          <h1 className="text-2xl font-bold" style={{ color: '#004C99' }}>TruCon Onboarding</h1>
        </div>
        <OnboardingStepper onFinish={() => router.push('/dashboard')} />
      </div>
    </div>
  )
}
