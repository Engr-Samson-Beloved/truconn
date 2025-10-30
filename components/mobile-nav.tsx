"use client"

import { usePathname } from "next/navigation"
import Link from "next/link"
import { Home, Users, Bell, User, Settings } from "lucide-react"

const navItems = [
  { href: "/", icon: Home, label: "Home" },
  { href: "/dashboard", icon: Users, label: "Requests" },
  { href: "/transparency", icon: Bell, label: "Verify" },
  { href: "/dashboard/transparency", icon: Settings, label: "History" },
  { href: "/profile", icon: User, label: "Profile" },
]

export function MobileNav() {
  const pathname = usePathname()

  return (
    <nav 
      className="fixed bottom-0 left-0 right-0 border-t md:hidden z-40 animate-slide-up"
      style={{ 
        background: '#FFFFFF',
        borderColor: '#E0E4E8'
      }}
    >
      <div className="flex items-center justify-around h-16">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              className="flex flex-col items-center justify-center w-full h-full relative transition-colors"
            >
              <div 
                className="relative transition-colors"
                style={{ color: isActive ? '#004C99' : '#8B95A1' }}
              >
                <Icon className="w-6 h-6" />
              </div>
              <span 
                className="text-xs mt-1 font-medium"
                style={{ color: isActive ? '#004C99' : '#8B95A1' }}
              >
                {item.label}
              </span>
              {isActive && (
                <div 
                  className="absolute bottom-0 left-0 right-0 h-1 animate-slide-up rounded-t-full"
                  style={{ background: '#004C99' }}
                />
              )}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
