import { useEffect, useState } from "react";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "./lib/supabaseClient";

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
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
    });
    if (error) alert(error.message);
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) alert(error.message);
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
        </>
      )}
    </div>
  );
}