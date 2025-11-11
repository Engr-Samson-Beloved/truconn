import { getApiHeaders } from "@/lib/utils"
import { ApiInterceptor } from "@/lib/api-interceptor"

const API_BASE_URL = "https://truconn.onrender.com/api"

export interface ComplianceViolation {
  rule: string
  details: Record<string, any>
  recommendation: string
}

export interface ComplianceAudit {
  id: number
  organization: number
  organization_name: string
  rule_name: string
  rule_description: string
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  status: "PENDING" | "RESOLVED" | "INVESTIGATING" | "IGNORED"
  detected_at: string
  resolved_at?: string
  details: Record<string, any>
  recommendation: string
}

export interface ComplianceScanResult {
  risk_score: number
  total_violations: number
  critical_count: number
  high_count: number
  medium_count: number
  violations: ComplianceViolation[]
  audit_records?: ComplianceAudit[]
}

export interface ComplianceReport {
  organization: {
    id: number
    name: string
  }
  statistics: {
    total_audits: number
    pending_audits: number
    resolved_audits: number
    unresolved_violations: number
  }
  audits: ComplianceAudit[]
  violations: Array<{
    id: number
    violation_type: string
    description: string
    detected_at: string
    resolved: boolean
  }>
}

export class ComplianceAPI {
  /**
   * Run compliance scan for organization
   * POST /api/compliance/scan/
   */
  static async runScan(): Promise<{ message: string; data: ComplianceScanResult }> {
    try {
      const response = await fetch(`${API_BASE_URL}/compliance/scan/`, {
        method: "POST",
        headers: getApiHeaders(),
        credentials: "include",
      })

      if (!response.ok) {
        if (response.status === 401) {
          await ApiInterceptor.handleSessionExpired()
          throw new Error("Your session has expired. Please log in again.")
        }
        if (response.status === 502) {
          throw new Error("Backend service is currently unavailable. Please try again later.")
        }

        let errorData
        try {
          errorData = await response.json()
        } catch {
          throw new Error(`Failed to run compliance scan: ${response.status}`)
        }

        const errorMessage = errorData.error || errorData.detail || errorData.message || "Failed to run compliance scan"
        throw new Error(errorMessage)
      }

      // Update activity on successful API call
      const data = await response.json()
      if (typeof window !== "undefined") {
        const now = Date.now()
        localStorage.setItem('last_activity', now.toString())
      }
      return data
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Failed to connect to server. Please check your internet connection.")
      }
      throw error
    }
  }

  /**
   * Get latest compliance scan results
   * GET /api/compliance/scan/
   */
  static async getScanResults(): Promise<ComplianceScanResult & { audits: ComplianceAudit[] }> {
    try {
      const response = await fetch(`${API_BASE_URL}/compliance/scan/`, {
        method: "GET",
        headers: getApiHeaders(),
        credentials: "include",
      })

      if (!response.ok) {
        if (response.status === 401) {
          await ApiInterceptor.handleSessionExpired()
          throw new Error("Your session has expired. Please log in again.")
        }
        if (response.status === 502) {
          throw new Error("Backend service is currently unavailable. Please try again later.")
        }

        let errorData
        try {
          errorData = await response.json()
        } catch {
          throw new Error(`Failed to get compliance scan results: ${response.status}`)
        }

        const errorMessage = errorData.error || errorData.detail || errorData.message || "Failed to get compliance scan results"
        throw new Error(errorMessage)
      }

      // Update activity on successful API call
      const data = await response.json()
      if (typeof window !== "undefined") {
        const now = Date.now()
        localStorage.setItem('last_activity', now.toString())
      }
      return data
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Failed to connect to server. Please check your internet connection.")
      }
      throw error
    }
  }

  /**
   * Get compliance reports
   * GET /api/compliance/reports/
   */
  static async getReports(orgId?: number): Promise<ComplianceReport> {
    try {
      const url = orgId 
        ? `${API_BASE_URL}/compliance/reports/${orgId}/`
        : `${API_BASE_URL}/compliance/reports/`
      
      const response = await fetch(url, {
        method: "GET",
        headers: getApiHeaders(),
        credentials: "include",
      })

      if (!response.ok) {
        if (response.status === 401) {
          await ApiInterceptor.handleSessionExpired()
          throw new Error("Your session has expired. Please log in again.")
        }
        if (response.status === 502) {
          throw new Error("Backend service is currently unavailable. Please try again later.")
        }

        let errorData
        try {
          errorData = await response.json()
        } catch {
          throw new Error(`Failed to get compliance reports: ${response.status}`)
        }

        const errorMessage = errorData.error || errorData.detail || errorData.message || "Failed to get compliance reports"
        throw new Error(errorMessage)
      }

      // Update activity on successful API call
      const data = await response.json()
      if (typeof window !== "undefined") {
        const now = Date.now()
        localStorage.setItem('last_activity', now.toString())
      }
      return data
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Failed to connect to server. Please check your internet connection.")
      }
      throw error
    }
  }

  /**
   * Update audit status
   * PATCH /api/compliance/audit/<audit_id>/
   */
  static async updateAuditStatus(auditId: number, status: string): Promise<{ message: string; data: ComplianceAudit }> {
    try {
      const response = await fetch(`${API_BASE_URL}/compliance/audit/${auditId}/`, {
        method: "PATCH",
        headers: {
          ...getApiHeaders(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status }),
        credentials: "include",
      })

      if (!response.ok) {
        if (response.status === 401) {
          await ApiInterceptor.handleSessionExpired()
          throw new Error("Your session has expired. Please log in again.")
        }
        if (response.status === 502) {
          throw new Error("Backend service is currently unavailable. Please try again later.")
        }

        let errorData
        try {
          errorData = await response.json()
        } catch {
          throw new Error(`Failed to update audit status: ${response.status}`)
        }

        const errorMessage = errorData.error || errorData.detail || errorData.message || "Failed to update audit status"
        throw new Error(errorMessage)
      }

      // Update activity on successful API call
      const data = await response.json()
      if (typeof window !== "undefined") {
        const now = Date.now()
        localStorage.setItem('last_activity', now.toString())
      }
      return data
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Failed to connect to server. Please check your internet connection.")
      }
      throw error
    }
  }
}


