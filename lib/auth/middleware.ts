import { NextResponse, type NextRequest } from "next/server"

// Public routes that don't require authentication
const publicRoutes = [
  "/",
  "/login",
  "/signup",
  "/get-started",
  "/transparency",
  "/learn",
  "/help",
]

export async function checkAuth(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Allow public routes
  if (publicRoutes.some((route) => pathname === route || pathname.startsWith(route + "/"))) {
    return NextResponse.next({
      request,
    })
  }

  // Check for auth token in cookies (for server-side)
  // Since middleware runs on server, we check cookies
  const authCookie = request.cookies.get("truconn_user")

  // If no auth cookie and trying to access protected route, redirect to login
  // Note: We allow the request through for client-side auth checks as well
  // This provides a soft redirect, but client components will handle auth state
  if (!authCookie && !publicRoutes.some((route) => pathname === route || pathname.startsWith(route + "/"))) {
    // Only redirect if it's a protected route
    const url = request.nextUrl.clone()
    url.pathname = "/login"
    // Store the intended destination for redirect after login
    url.searchParams.set("redirect", pathname)
    return NextResponse.redirect(url)
  }

  return NextResponse.next({
    request,
  })
}

