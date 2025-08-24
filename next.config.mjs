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
  // Remove standalone output for Vercel - not needed
  // outputFileTracingRoot: process.cwd(), // Not needed for Vercel
}

export default nextConfig
