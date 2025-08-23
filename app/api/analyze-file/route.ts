import { type NextRequest, NextResponse } from "next/server"
import type { PactGuardAnalysisReport } from "@/types"

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get("file") as File

    if (!file) {
      return NextResponse.json({ error: "File is required" }, { status: 400 })
    }

    // Forward to backend
    const backendFormData = new FormData()
    backendFormData.append("file", file)

    const backendResponse = await fetch(`${BACKEND_URL}/analyze-file`, {
      method: "POST",
      body: backendFormData,
    })

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ error: "Backend error" }))
      console.error("Backend file analysis failed:", errorData)
      return NextResponse.json(
        { error: errorData.detail || "File analysis failed" }, 
        { status: backendResponse.status }
      )
    }

    // The backend now returns the correct structure, so no transformation is needed.
    const backendResult: PactGuardAnalysisReport = await backendResponse.json()

    return NextResponse.json(backendResult)
  } catch (error) {
    console.error("File analysis API error:", error)
    return NextResponse.json({ error: "Failed to analyze file" }, { status: 500 })
  }
}
