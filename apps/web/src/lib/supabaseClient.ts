import { createClient } from "@supabase/supabase-js";

/**
 * 브라우저용 Supabase Client
 * - anon key는 클라이언트에서 사용 가능한 공개 키
 * - 데이터 접근 제어는 Supabase RLS로 강제한다.
 */
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error("Missing VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY");
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);