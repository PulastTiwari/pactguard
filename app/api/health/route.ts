import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Check if backend is reachable
    const backendUrl = process.env.NODE_ENV === 'production' 
      ? 'http://backend:8000/health'
      : 'http://localhost:8001/health'
    
    const backendResponse = await fetch(backendUrl, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    
    const backendHealth = backendResponse.ok
    
    return NextResponse.json({
      status: 'healthy',
      frontend: 'running',
      backend: backendHealth ? 'healthy' : 'unreachable',
      timestamp: new Date().toISOString(),
      service: 'pactguard-frontend'
    })
  } catch (error) {
    return NextResponse.json({
      status: 'degraded',
      frontend: 'running', 
      backend: 'unreachable',
      error: 'Backend health check failed',
      timestamp: new Date().toISOString(),
      service: 'pactguard-frontend'
    }, { status: 503 })
  }
}
