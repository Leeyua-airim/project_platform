import { useEffect, useState } from "react";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "./lib/supabaseClient";
import { fetchMe } from "./lib/api"; // 추가

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [meResult, setMeResult] = useState<unknown>(null); // 추가
  const [meError, setMeError] = useState(""); // 추가
  const email = session?.user?.email ?? "";

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session ?? null);
    });

    const { data: sub } = supabase.auth.onAuthStateChange((_event, newSession) => {
      setSession(newSession);
    });

    return () => sub.subscription.unsubscribe();
  }, []);

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: window.location.origin,
      },
    });
    if (error) alert(error.message);
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) alert(error.message);

    setMeResult(null); // 추가
    setMeError(""); // 추가
  };

  const handleTestMe = async () => { // 추가
    try {
      const data = await fetchMe();
      setMeResult(data);
      setMeError("");
    } catch (error) {
      setMeResult(null);
      setMeError(error instanceof Error ? error.message : "Unknown error");
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>Project Platform</h1>

      {!session ? (
        <>
          <p>로그인이 필요합니다.</p>
          <button onClick={signInWithGoogle}>Google로 로그인</button>
        </>
      ) : (
        <>
          <p>로그인됨: {email}</p>
          <button onClick={signOut}>로그아웃</button>
          <button onClick={handleTestMe} style={{ marginLeft: 8 }}>
            /api/me 테스트
          </button>

          {meError ? <pre>{meError}</pre> : null}
          {meResult ? <pre>{JSON.stringify(meResult, null, 2)}</pre> : null}
        </>
      )}
    </div>
  );
}