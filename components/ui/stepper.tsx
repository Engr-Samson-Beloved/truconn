import * as React from 'react'

import { cn } from '@/lib/utils'

type Step = {
  id: string
  title: string
  description?: string
}

interface StepperProps {
  steps: Step[]
  currentStep: number
  onStepChange?: (index: number) => void
  className?: string
}

export function Stepper({ steps, currentStep, onStepChange, className }: StepperProps) {
  return (
    <div className={cn('w-full', className)}>
      <ol className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        {steps.map((step, index) => {
          const isActive = index === currentStep
          const isCompleted = index < currentStep
          return (
            <li key={step.id} className="flex items-start gap-3">
              <button
                type="button"
                onClick={() => onStepChange?.(index)}
                className={cn(
                  'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center border-2 transition-colors',
                  isCompleted && 'border-emerald-500 text-emerald-600',
                  isActive && 'border-[#004C99] text-[#004C99]',
                  !isActive && !isCompleted && 'border-[#E0E4E8] text-[#8B95A1]'
                )}
                aria-current={isActive ? 'step' : undefined}
              >
                {isCompleted ? '✓' : index + 1}
              </button>
              <div>
                <div className={cn('text-sm font-semibold', isActive ? 'text-[#004C99]' : 'text-[#222222]')}>{step.title}</div>
                {step.description && (
                  <div className="text-xs text-[#4A4A4A] mt-0.5">{step.description}</div>
                )}
              </div>
            </li>
          )
        })}
      </ol>
    </div>
  )
}
