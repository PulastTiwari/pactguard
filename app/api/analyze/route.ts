import { type NextRequest, NextResponse } from "next/server"
import type { PactGuardAnalysisReport } from "@/types"

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    if (!text || typeof text !== "string") {
      return NextResponse.json({ error: "Text content is required" }, { status: 400 })
    }

    console.log("🔥 Frontend API: Sending request to Portia backend")
    console.log(`   📡 Backend URL: ${BACKEND_URL}/analyze`)
    console.log(`   📄 Document length: ${text.length} characters`)

    // Call the Portia-powered backend API
    const backendResponse = await fetch(`${BACKEND_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    })

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ error: "Backend error" }))
      console.error("❌ Portia backend analysis failed:", errorData)
      return NextResponse.json(
        { error: errorData.detail || "Analysis failed" }, 
        { status: backendResponse.status }
      )
    }

    // Get the structured analysis from our Portia backend
    const backendResult: PactGuardAnalysisReport = await backendResponse.json()
    
    console.log("✅ Portia analysis completed successfully!")
    console.log(`   📋 Plan Run ID: ${backendResult.portia_integration?.plan_run_id || 'N/A'}`)
    console.log(`   🎯 Portia status: ${backendResult.portia_integration?.status}`)
    
    return NextResponse.json(backendResult)
  } catch (error) {
    console.error("❌ Frontend API error:", error)
    return NextResponse.json({ error: "Failed to analyze document" }, { status: 500 })
  }
}
