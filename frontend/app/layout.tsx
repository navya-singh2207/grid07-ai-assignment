import "./globals.css";
import Link from "next/link";
import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div style={{ background: "#1e3a8a", color: "white", padding: "14px 0" }}>
          <div className="container" style={{ display: "flex", gap: 18 }}>
            <Link href="/">Colleges</Link>
            <Link href="/compare">Compare</Link>
            <Link href="/predictor">Predictor</Link>
          </div>
        </div>
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
