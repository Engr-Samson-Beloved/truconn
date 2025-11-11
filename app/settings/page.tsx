"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"
import { Settings, Bell, Lock, Eye, LogOut, FileDown, Trash2, Globe } from "lucide-react"
import { CitizenSidebar } from "@/components/citizen-sidebar"
import { OrganizationSidebar } from "@/components/organization-sidebar"
import { useAuth } from "@/lib/auth/context"

export default function SettingsPage() {
  const router = useRouter()
  const { logout, user } = useAuth()
  const [settings, setSettings] = useState({
    emailNotifications: true,
    pushNotifications: false,
    privateProfile: false,
    twoFactorAuth: false,
    notificationFrequency: 'immediate',
    dataRetention: '12_months',
    language: 'en',
  })

  const toggleSetting = (key: keyof typeof settings) => {
    setSettings((prev) => ({ ...prev, [key]: typeof prev[key] === 'boolean' ? !prev[key] : prev[key] }))
  }

  // Determine which sidebar to use based on user role
  const SidebarComponent = user?.role === "organization" || user?.role === "ORGANIZATION" 
    ? OrganizationSidebar 
    : CitizenSidebar

  return (
    <div className="flex h-screen bg-background">
      <SidebarComponent />
      <main className="flex-1 overflow-auto">
        <div className="max-w-2xl mx-auto p-4 md:p-8">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-3 rounded-lg" style={{ background: '#004C991A' }}>
              <Settings className="w-6 h-6" style={{ color: '#004C99' }} />
            </div>
            <h1 className="text-3xl font-bold text-foreground">Settings</h1>
          </div>

          <div className="space-y-6">
            {/* Notifications Section */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Bell className="w-5 h-5" style={{ color: '#004C99' }} />
                <h2 className="text-lg font-semibold text-foreground">NDPR Notification Preferences</h2>
              </div>
              <div className="space-y-4">
                <label className="flex items-center justify-between cursor-pointer">
                  <span className="text-foreground">Email Notifications</span>
                  <input type="checkbox" checked={settings.emailNotifications} onChange={() => toggleSetting('emailNotifications')} className="w-5 h-5 rounded" />
                </label>
                <label className="flex items-center justify-between cursor-pointer">
                  <span className="text-foreground">Push Notifications</span>
                  <input type="checkbox" checked={settings.pushNotifications} onChange={() => toggleSetting('pushNotifications')} className="w-5 h-5 rounded" />
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">Notification Frequency</label>
                    <select
                      className="w-full border rounded-md px-3 py-2"
                      value={settings.notificationFrequency}
                      onChange={(e) => setSettings({ ...settings, notificationFrequency: e.target.value })}
                    >
                      <option value="immediate">Immediate</option>
                      <option value="daily">Daily Summary</option>
                      <option value="weekly">Weekly Summary</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm text-muted-foreground mb-1">Language</label>
                    <div className="flex items-center gap-2">
                      <Globe className="w-4 h-4 text-muted-foreground" />
                      <select
                        className="w-full border rounded-md px-3 py-2"
                        value={settings.language}
                        onChange={(e) => setSettings({ ...settings, language: e.target.value })}
                      >
                        <option value="en">English</option>
                        <option value="ha">Hausa (soon)</option>
                        <option value="yo">Yorùbá (soon)</option>
                        <option value="ig">Igbo (soon)</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Privacy Section */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Eye className="w-5 h-5 text-green-600" />
                <h2 className="text-lg font-semibold text-foreground">Privacy</h2>
              </div>
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-foreground">Private Profile</span>
                <input type="checkbox" checked={settings.privateProfile} onChange={() => toggleSetting('privateProfile')} className="w-5 h-5 rounded" />
              </label>
            </motion.div>

            {/* Security Section */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Lock className="w-5 h-5 text-red-600" />
                <h2 className="text-lg font-semibold text-foreground">Security</h2>
              </div>
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-foreground">Two-Factor Authentication</span>
                <input type="checkbox" checked={settings.twoFactorAuth} onChange={() => toggleSetting('twoFactorAuth')} className="w-5 h-5 rounded" />
              </label>
            </motion.div>

            {/* Data Management Section */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <FileDown className="w-5 h-5" style={{ color: '#004C99' }} />
                <h2 className="text-lg font-semibold text-foreground">Data Management</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button className="px-4 py-2 border rounded-md text-left hover:bg-muted transition" title="Export Data Report (PDF placeholder)">
                  Export Data Report (PDF)
                </button>
                <div>
                  <label className="block text-sm text-muted-foreground mb-1">Data Retention</label>
                  <select
                    className="w-full border rounded-md px-3 py-2"
                    value={settings.dataRetention}
                    onChange={(e) => setSettings({ ...settings, dataRetention: e.target.value })}
                  >
                    <option value="6_months">6 months</option>
                    <option value="12_months">12 months</option>
                    <option value="24_months">24 months</option>
                  </select>
                </div>
              </div>
            </motion.div>

            {/* Account Deletion Request */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Trash2 className="w-5 h-5 text-red-600" />
                <h2 className="text-lg font-semibold text-foreground">Account Deletion Request</h2>
              </div>
              <p className="text-sm text-muted-foreground mb-3">Request deletion of your account and associated data. This action is irreversible.</p>
              <button className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition">Request Deletion</button>
            </motion.div>

            {/* Logout */}
            <motion.button
              onClick={async () => {
                try {
                  await logout()
                  window.location.href = "/login"
                } catch (error) {
                  window.location.href = "/login"
                }
              }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition-colors"
            >
              <LogOut className="w-5 h-5" />
              Logout
            </motion.button>
          </div>
        </div>
      </main>
    </div>
  )
}
