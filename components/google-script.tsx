"use client"

import { useEffect } from 'react'

export default function GoogleScript() {
  useEffect(() => {
    // Load Google OAuth script dynamically on client side only
    if (typeof window !== 'undefined' && !document.querySelector('script[src*="accounts.google.com"]')) {
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      document.head.appendChild(script)
    }
  }, [])

  return null
}
