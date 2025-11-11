import { getApiHeaders } from "@/lib/utils"

const API_BASE_URL = "https://truconn.onrender.com/api"

export interface Consent {
  id: number
  name: string
  created_at?: string
}

export interface UserConsentResponse {
  consent: string
  access: boolean
}

export class ConsentsAPI {
  /**
   * Get all available consent categories
   * GET /api/consents/
   */
  static async getConsents(): Promise<Consent[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/consents/`, {
        method: "GET",
        headers: getApiHeaders(),
        credentials: "include", // Include cookies for session auth
      })

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Please log in to view consents")
        }
        if (response.status === 502) {
          throw new Error("Backend service is currently unavailable. Please try again later.")
        }
        
        let errorData
        try {
          errorData = await response.json()
        } catch {
          throw new Error(`Failed to fetch consents: ${response.status}`)
        }
        
        const errorMessage = errorData.error || errorData.detail || errorData.message || "Failed to fetch consents"
        throw new Error(errorMessage)
      }

      return await response.json()
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Failed to connect to server. Please check your internet connection.")
      }
      throw error
    }
  }

  /**
   * Toggle consent (grant or revoke)
   * POST /api/consents/<consent_id>/toggle/
   */
  static async toggleConsent(consentId: number): Promise<UserConsentResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/consents/${consentId}/toggle/`, {
        method: "POST",
        headers: getApiHeaders(),
        credentials: "include", // Include cookies for session auth
      })

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Please log in to manage consents")
        }
        if (response.status === 502) {
          throw new Error("Backend service is currently unavailable. Please try again later.")
        }
        
        let errorData
        try {
          errorData = await response.json()
        } catch {
          throw new Error(`Failed to toggle consent: ${response.status}`)
        }
        
        const errorMessage = errorData.error || errorData.detail || errorData.message || "Failed to toggle consent"
        throw new Error(errorMessage)
      }

      return await response.json()
    } catch (error) {
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Failed to connect to server. Please check your internet connection.")
      }
      throw error
    }
  }
}


