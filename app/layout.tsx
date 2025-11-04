import type React from "react"
import { Inter } from "next/font/google"
import "./globals.css"
import { MobileNav } from "@/components/mobile-nav"
import { AuthProvider } from "@/lib/auth/context"

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "TruCon - Where Trust Meets Connection",
  description: "A professional trust-based connection platform",
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-background text-foreground pb-16 md:pb-0`}>
        <AuthProvider>
          {children}
          <MobileNav />
        </AuthProvider>
      </body>
    </html>
  )
}
