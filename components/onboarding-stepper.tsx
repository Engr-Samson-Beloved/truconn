"use client"

import * as React from 'react'
import { Stepper } from '@/components/ui/stepper'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { DataCategory, DataCategorySelector } from '@/components/data-category-selector'

interface OnboardingData {
  name: string
  email: string
  nin?: string
  password: string
  categories: DataCategory[]
  consentAccepted: boolean
}

interface OnboardingStepperProps {
  onFinish?: (data: OnboardingData) => void
}

export function OnboardingStepper({ onFinish }: OnboardingStepperProps) {
  const [step, setStep] = React.useState(0)
  const [data, setData] = React.useState<OnboardingData>({
    name: '',
    email: '',
    nin: '',
    password: '',
    categories: [],
    consentAccepted: false,
  })

  const steps = [
    { id: 'welcome', title: 'Welcome', description: 'Your Data. Your Choice. Your Trust.' },
    { id: 'info', title: 'Personal Info', description: 'Enter your basic details' },
    { id: 'categories', title: 'Data Categories', description: 'Choose what you manage' },
    { id: 'consent', title: 'Consent', description: 'Acknowledge data terms' },
  ]

  const canContinue = () => {
    if (step === 0) return true
    if (step === 1) return data.name && data.email && data.password.length >= 8
    if (step === 2) return data.categories.length > 0
    if (step === 3) return data.consentAccepted
    return false
  }

  const next = () => {
    if (step < steps.length - 1) setStep(step + 1)
    else onFinish?.(data)
  }

  const back = () => setStep(Math.max(0, step - 1))

  return (
    <div className="max-w-2xl mx-auto">
      <Stepper steps={steps} currentStep={step} onStepChange={setStep} className="mb-8" />

      {/* Step Content */}
      <div className="bg-white border border-[#E0E4E8] rounded-lg p-6">
        {step === 0 && (
          <div className="text-center space-y-3">
            <h2 className="text-2xl font-bold" style={{ color: '#004C99' }}>Welcome to TruCon</h2>
            <p className="text-[#4A4A4A]">A transparent, trust-first platform for data consent and verification.</p>
            <div className="mt-4 text-left bg-[#F7F9FB] border border-[#E0E4E8] rounded-md p-4">
              <p className="text-sm" style={{ color: '#222222' }}>
                TruCon does not access your personal information without your explicit consent. You decide what is shared,
                with whom, and for how long. You can revoke access at any time, and every action is recorded in your
                Transparency Log.
              </p>
            </div>
          </div>
        )}

        {step === 1 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: '#222222' }}>Full Name</label>
              <Input value={data.name} onChange={(e) => setData({ ...data, name: e.target.value })} placeholder="Jane Doe" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: '#222222' }}>Email</label>
              <Input type="email" value={data.email} onChange={(e) => setData({ ...data, email: e.target.value })} placeholder="you@example.com" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: '#222222' }}>NIN (optional)</label>
              <Input value={data.nin} onChange={(e) => setData({ ...data, nin: e.target.value })} placeholder="1234 5678 9012" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: '#222222' }}>Password</label>
              <Input type="password" value={data.password} onChange={(e) => setData({ ...data, password: e.target.value })} placeholder="••••••••" />
            </div>
            <div className="text-xs mt-2" style={{ color: '#4A4A4A' }}>
              Your account details are encrypted and used only to secure access to your dashboard. TruCon will never sell
              your data.
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <p className="text-sm" style={{ color: '#4A4A4A' }}>Select the data categories you want to manage under TruCon.</p>
            <DataCategorySelector value={data.categories} onChange={(categories) => setData({ ...data, categories })} />
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <p className="text-sm" style={{ color: '#4A4A4A' }}>
              By proceeding, you acknowledge that TruCon processes your data in accordance with the Nigeria Data Protection
              Regulation (NDPR). You may revoke consent at any time.
            </p>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={data.consentAccepted} onChange={(e) => setData({ ...data, consentAccepted: e.target.checked })} />
              <span className="text-sm" style={{ color: '#222222' }}>I consent to TruCon’s data terms.</span>
            </label>
          </div>
        )}

        <div className="flex justify-between mt-6">
          <Button type="button" variant="outline" onClick={back} disabled={step === 0}>Back</Button>
          <Button type="button" onClick={next} disabled={!canContinue()}>{step === steps.length - 1 ? 'Finish' : 'Continue'}</Button>
        </div>
      </div>
    </div>
  )
}
