import { createBrowserClient } from "@supabase/ssr"

// Temporary: Mock Supabase client when env vars are not set
export function createClient() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

  // If env vars are missing, return a mock client
  if (!supabaseUrl || !supabaseKey) {
    return {
      auth: {
        signInWithPassword: async () => ({ data: { user: null }, error: null }),
        signUp: async () => ({ data: { user: null }, error: null }),
        getUser: async () => ({ data: { user: null }, error: null }),
        signOut: async () => ({ error: null }),
      },
      from: (table: string) => ({
        select: () => ({
          data: [],
          error: null,
          order: () => ({ data: [], error: null }),
        }),
        insert: () => ({ data: null, error: null }),
        update: () => ({ data: null, error: null }),
        delete: () => ({ data: null, error: null }),
      }),
    } as any
  }

  return createBrowserClient(supabaseUrl, supabaseKey)
}
