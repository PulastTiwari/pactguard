import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { ThemeProvider } from "../components/theme-provider"
import "./globals.css"

export const metadata: Metadata = {
  title: "PactGuard - Legal Document Analyzer",
  description: "Transform complex legal documents into simple, scannable nutrition labels with AI",
  generator: "v0.app",
  keywords: "legal document analysis, AI legal assistant, terms of service analyzer, privacy policy checker",
  authors: [{ name: "PactGuard Team" }],
}

export const viewport = {
  width: "device-width",
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <style>{`
html {
  font-family: ${GeistSans.style.fontFamily};
  --font-sans: ${GeistSans.variable};
  --font-mono: ${GeistMono.variable};
}
        `}</style>
      </head>
      <body className={`${GeistSans.variable} ${GeistMono.variable} antialiased`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <div className="min-h-screen bg-background text-foreground">
            <main className="container mx-auto px-4 py-6 sm:py-8 lg:py-12 max-w-5xl">{children}</main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
