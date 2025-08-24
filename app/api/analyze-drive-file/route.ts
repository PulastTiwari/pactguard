import { NextRequest, NextResponse } from 'next/server'
import { convertToLegacyFormat } from '@/lib/format-converter'
import type { PactGuardAnalysisReport } from '@/types'

export async function POST(request: NextRequest) {
  console.log('📁 Google Drive analysis request received')
  
  try {
    const body = await request.json()
    console.log('📁 Request body:', body)
    
    // Forward the request to the backend
    const backendResponse = await fetch('http://localhost:8001/analyze-drive-file', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
    
    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ error: 'Backend request failed' }))
      console.error('❌ Backend error:', errorData)
      return NextResponse.json(
        { error: errorData.detail || errorData.error || 'Google Drive analysis failed' },
        { status: backendResponse.status }
      )
    }
    
    const backendResult: PactGuardAnalysisReport = await backendResponse.json()
    console.log('✅ Google Drive analysis successful:', backendResult.id)
    
    // Convert to legacy format
    const convertedResult = convertToLegacyFormat(backendResult)
    
    return NextResponse.json(convertedResult)
    
  } catch (error) {
    console.error('❌ Google Drive analysis error:', error)
    return NextResponse.json(
      { error: 'Internal server error during Google Drive analysis' },
      { status: 500 }
    )
  }
}
