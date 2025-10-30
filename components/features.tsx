"use client"

import { motion } from "framer-motion"
import { Shield, Eye, FileCheck } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const features = [
  {
    icon: Shield,
    title: "Consent Management",
    description:
      "Take full control of your personal data. Grant, modify, or revoke consent with clear transparency on what data is shared and with whom.",
    color: "#004C99",
  },
  {
    icon: Eye,
    title: "Transparency Dashboard",
    description:
      "Real-time visibility into how your data is being accessed. View detailed logs of every organization that accesses your information and when.",
    color: "#00B38F",
  },
  {
    icon: FileCheck,
    title: "Compliance Engine",
    description:
      "Organizations get automated compliance monitoring under NDPR standards. Receive alerts and recommendations to maintain data protection standards.",
    color: "#F9C80E",
  },
]

export function Features() {
  return (
    <section id="features" className="py-20 md:py-32 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4" style={{ color: '#004C99', fontWeight: 700 }}>
            Empowered Data Control
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: '#4A4A4A', lineHeight: '1.6' }}>
            Your right to data privacy and control. See, manage, and protect your personal information with complete
            transparency.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Card 
                  className="h-full card-hover group"
                  style={{ 
                    border: '2px solid #E0E4E8',
                    background: '#FFFFFF'
                  }}
                >
                  <CardHeader className="space-y-4">
                    <div className="relative">
                      <div 
                        className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl transition-transform duration-300 group-hover:scale-110"
                        style={{ 
                          background: `${feature.color}15`
                        }}
                      >
                        <Icon className="w-8 h-8" style={{ color: feature.color }} />
                      </div>
                    </div>
                    <CardTitle 
                      className="text-xl font-bold mb-2"
                      style={{ color: '#222222', fontWeight: 600 }}
                    >
                      {feature.title}
                    </CardTitle>
                    <CardDescription 
                      className="text-base leading-relaxed"
                      style={{ color: '#4A4A4A', lineHeight: '1.6' }}
                    >
                      {feature.description}
                    </CardDescription>
                  </CardHeader>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
