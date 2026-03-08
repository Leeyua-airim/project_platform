// Django API 호출 함수 모음
// 현재 로그인한 Supabase 세션의 access token을 Authorization 헤더에 담아 보냄

import { supabase } from "./supabaseClient";

export async function fetchMe() {
  // 현재 로그인 세션 조회
  const {
    data: { session },
  } = await supabase.auth.getSession();

  const token = session?.access_token;

  // 로그인 안 된 상태면 호출 불가
  if (!token) {
    throw new Error("No access token");
  }

  // Django /api/me 호출
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  // 실패 시 응답 본문까지 같이 확인
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  return response.json();
}