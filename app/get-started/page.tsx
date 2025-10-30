"use client"

import { motion } from "framer-motion"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Shield, Eye, FileCheck } from "lucide-react"

export default function GetStartedPage() {
  const features = [
    { icon: Shield, color: '#004C99', title: 'Consent You Control', description: 'Grant or revoke access by category: Financial, Biometric, Health, Identity.' },
    { icon: Eye, color: '#00B38F', title: 'Full Transparency', description: 'See who accessed your data, when, and why — in real time.' },
    { icon: FileCheck, color: '#F9C80E', title: 'Built for NDPR', description: 'Compliance-first workflows aligned to Nigeria’s data laws.' },
  ]

  const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.2 } } }
  const itemVariants = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } } }

  return (
    <div className="min-h-screen" style={{ background: '#F7F9FB' }}>
      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <h1 className="text-5xl font-bold mb-6" style={{ color: '#004C99' }}>Your Data. Your Choice. Your Trust.</h1>
          <p className="text-xl mb-8 mx-auto max-w-2xl" style={{ color: '#4A4A4A' }}>
            TruCon NDTS empowers Nigerians with transparent consent and secure data verification, built for NDPR.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/onboarding">
              <Button size="lg" className="px-8">Start Onboarding</Button>
            </Link>
            <Link href="/signup">
              <Button size="lg" variant="outline" className="px-8">Create Account</Button>
            </Link>
          </div>
        </motion.div>

        {/* Features Grid */}
        <motion.div className="grid md:grid-cols-3 gap-8 mt-20" variants={containerVariants} initial="hidden" animate="visible">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <motion.div key={index} className="p-8 rounded-lg bg-white border" style={{ borderColor: '#E0E4E8' }} variants={itemVariants}>
                <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style={{ background: `${feature.color}1A` }}>
                  <Icon className="w-7 h-7" style={{ color: feature.color }} />
                </div>
                <h3 className="text-lg font-semibold" style={{ color: '#222222' }}>{feature.title}</h3>
                <p className="text-[#4A4A4A] mt-1">{feature.description}</p>
              </motion.div>
            )
          })}
        </motion.div>
      </section>

      {/* Assurance Section */}
      <section className="py-20" style={{ background: '#FFFFFF' }}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6" style={{ color: '#004C99' }}>Built for Nigerians. Powered by Trust.</h2>
          <p className="text-lg mx-auto max-w-2xl" style={{ color: '#4A4A4A' }}>
            Designed with government-level reliability and citizen-first transparency. Calm motion, clear hierarchy, and consistent UI build confidence.
          </p>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <h2 className="text-3xl font-bold mb-6" style={{ color: '#004C99' }}>Ready to take control?</h2>
        <p className="text-xl mb-8 mx-auto max-w-2xl" style={{ color: '#4A4A4A' }}>
          Start the onboarding flow to set your preferences and manage your data trusts.
        </p>
        <Link href="/onboarding">
          <Button size="lg" className="px-8">Begin Now</Button>
        </Link>
      </section>
    </div>
  )
}
