import { type NextRequest, NextResponse } from "next/server"
import type { PactGuardAnalysisReport } from "@/types"

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    if (!text || typeof text !== "string") {
      return NextResponse.json({ error: "Text content is required" }, { status: 400 })
    }

    // Call the real backend API
    const backendResponse = await fetch(`${BACKEND_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    })

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ error: "Backend error" }))
      console.error("Backend analysis failed:", errorData)
      return NextResponse.json(
        { error: errorData.detail || "Analysis failed" }, 
        { status: backendResponse.status }
      )
    }

    // The backend now returns the correct structure, so no transformation is needed.
    const backendResult: PactGuardAnalysisReport = await backendResponse.json()
    
    return NextResponse.json(backendResult)
  } catch (error) {
    console.error("Analysis API error:", error)
    return NextResponse.json({ error: "Failed to analyze document" }, { status: 500 })
  }
}
