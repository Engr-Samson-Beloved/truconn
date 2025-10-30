"use client"

import { motion } from "framer-motion"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, ShieldCheck } from "lucide-react"

export function Hero() {
  return (
    <section className="relative overflow-hidden py-20 md:py-32 lg:py-40 bg-gradient-to-br from-white via-blue-50/30 to-white">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-4xl mx-auto">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <div className="verified-badge">
              <ShieldCheck className="w-4 h-4" />
              <span>NDPR Compliant • Government Accredited</span>
            </div>
          </motion.div>

          {/* Main Heading - Official Tagline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6"
            style={{ color: '#004C99', fontWeight: 700 }}
          >
            Your Data.{" "}
            <span style={{ color: '#00B38F' }}>Your Choice.</span>{" "}
            <span style={{ color: '#F9C80E' }}>Your Trust.</span>
          </motion.h1>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg md:text-xl leading-relaxed max-w-3xl mx-auto mb-4"
            style={{ color: '#4A4A4A', lineHeight: '1.6' }}
          >
            A transparent, trust-first data consent and verification platform that empowers Nigerian citizens and 
            organizations to manage, verify, and consent to data usage securely.
          </motion.p>
          
          {/* Built for Nigerians */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="text-sm font-medium mb-8"
            style={{ color: '#00B38F' }}
          >
            Built for Nigerians. Powered by Trust.
          </motion.p>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4"
          >
            <Link href="/get-started">
              <button className="trust-button px-8 py-4 text-base flex items-center gap-2">
                Get Started
                <ArrowRight size={18} />
              </button>
            </Link>
            <Link href="#features">
              <button 
                className="px-8 py-4 rounded-lg font-semibold text-base transition-all duration-300 border-2"
                style={{ 
                  borderColor: '#004C99', 
                  color: '#004C99',
                  background: 'transparent'
                }}
              >
                Learn How TruCon Protects You
              </button>
            </Link>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mt-16 pt-8 border-t"
            style={{ borderColor: '#E0E4E8' }}
          >
            <p className="text-sm font-medium mb-6" style={{ color: '#4A4A4A' }}>
              Trusted by organizations across Nigeria
            </p>
            <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12">
              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: 'rgba(0, 76, 153, 0.1)' }}>
                  {/* Lucide Bank Icon for Banking */}
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7" style={{color:'#004C99'}} fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M3 11V7.5a2 2 0 0 1 1.106-1.788l7-3.5a2 2 0 0 1 1.788 0l7 3.5A2 2 0 0 1 21 7.5V11"/><path d="M19 21V11H5v10m2-5h10"/></svg>
                </div>
                <span className="text-sm font-medium" style={{ color: '#4A4A4A' }}>Banking</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: 'rgba(0, 179, 143, 0.1)' }}>
                  {/* Lucide Hospital Icon for Healthcare */}
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7" style={{color:'#00B38F'}} fill="none" viewBox="0 0 24 24" stroke="currentColor"><rect width="16" height="16" x="4" y="4" rx="2"/><path d="M9 12h6M12 9v6"/></svg>
                </div>
                <span className="text-sm font-medium" style={{ color: '#4A4A4A' }}>Healthcare</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: 'rgba(249, 200, 14, 0.15)' }}>
                  {/* Lucide Landmark Icon for Government */}
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7" style={{color:'#F9C80E'}} fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M3 22h18M6 18v-6M10 18v-6M14 18v-6M18 18v-6M4 10l8-6 8 6"/></svg>
                </div>
                <span className="text-sm font-medium" style={{ color: '#4A4A4A' }}>Government</span>
              </div>
              <div className="flex flex-col items-center gap-2">
                <div className="w-12 h-12 rounded-full flex items-center justify-center" style={{ background: 'rgba(0, 76, 153, 0.1)' }}>
                  {/* Lucide GraduationCap Icon for Education */}
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7" style={{color:'#004C99'}} fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M22 10.5V6c0-.379-.214-.725-.553-.895l-8-4a1 1 0 0 0-.894 0l-8 4A1 1 0 0 0 2 6v4.5"/><path d="M6 16v-1a6 6 0 0 1 12 0v1M18 10a6 6 0 1 1-12 0"/></svg>
                </div>
                <span className="text-sm font-medium" style={{ color: '#4A4A4A' }}>Education</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
