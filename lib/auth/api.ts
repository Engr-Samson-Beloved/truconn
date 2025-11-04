const API_BASE_URL = "https://truconn.onrender.com/api/auth"

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  first_name: string
  last_name: string
  email: string
  password1: string
  password2: string
  user_role: "CITIZEN" | "ORGANIZATION"
}

export interface User {
  id: string
  first_name: string
  last_name: string
  email: string
  role: string
}

export interface LoginResponse {
  user: User
}

export interface SignupResponse {
  user: {
    id: string
    first_name: string
    last_name: string
    email: string
    user_role: string
  }
  profile: {
    id: string
    user: string
    title: string
    company: string
    url: string
    phone_no: string
    about: string
    profile_pic: string | null
  }
}

export class AuthAPI {
  static async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: "Invalid email or password" }))
      throw new Error(errorData.error || errorData.detail || "Login failed")
    }

    return response.json()
  }

  static async signup(data: SignupData): Promise<SignupResponse> {
    const response = await fetch(`${API_BASE_URL}/signup/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: "Signup failed" }))
      const errorMessage = errorData.email?.[0] || errorData.password1?.[0] || errorData.non_field_errors?.[0] || errorData.error || "Signup failed"
      throw new Error(errorMessage)
    }

    return response.json()
  }
}

