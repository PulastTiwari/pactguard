/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false, // Enable for production
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    // Local development proxy so frontend fetch("/api/*") hits FastAPI backend on :8000
    // In production (Vercel) vercel.json handles this.
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8000/:path*'
        }
      ]
    }
    return []
  }
}

export default nextConfig
