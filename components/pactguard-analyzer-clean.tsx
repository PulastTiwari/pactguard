"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Sparkles, RotateCcw, Mail } from "lucide-react"
import { LoadingSpinner } from "@/components/ui/loading-spinner"
import type { AnalysisResult } from "@/types"
import AnalysisReport from "./analysis-report"
import { AnalysisSharing } from "@/lib/analysis-sharing"

export default function PactGuardAnalyzer() {
  const [text, setText] = useState("")
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError("Please enter some text to analyze")
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      })

      if (!response.ok) {
        throw new Error("Failed to analyze document")
      }

      const result: AnalysisResult = await response.json()
      setAnalysisResult(result)
      
      // Share analysis for email/other features
      AnalysisSharing.getInstance().shareAnalysis(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setText("")
    setAnalysisResult(null)
    setError(null)
    AnalysisSharing.getInstance().clearAnalysis()
  }

  const handleShareToEmail = () => {
    if (analysisResult) {
      AnalysisSharing.getInstance().shareAnalysis(analysisResult)
      // Scroll to advanced features section
      document.querySelector('[aria-label="Advanced analysis features"]')?.scrollIntoView({ 
        behavior: 'smooth' 
      })
      // Focus on email tab
      setTimeout(() => {
        const emailTab = document.querySelector('[data-state][value="email"]') as HTMLElement
        emailTab?.click()
      }, 500)
    }
  }

  const isAnalyzeDisabled = isLoading || !text.trim()

  return (
    <div className="space-y-6">
      <Card className="shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <FileText className="h-6 w-6 text-primary" aria-hidden="true" />
            <div>
              <CardTitle className="text-xl font-semibold">Document Analyzer</CardTitle>
              <CardDescription className="mt-1">
                Paste your legal document text below to get an AI-powered analysis
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="document-text" className="text-sm font-medium text-foreground">
              Document Text
            </label>
            <Textarea
              id="document-text"
              placeholder="Paste your terms of service, privacy policy, or any legal document here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="min-h-[200px] resize-none text-sm leading-relaxed"
              disabled={isLoading}
              aria-describedby={error ? "error-message" : undefined}
            />
          </div>

          {error && (
            <div
              id="error-message"
              className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg"
              role="alert"
              aria-live="polite"
            >
              <p className="text-sm text-destructive font-medium">{error}</p>
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            <Button onClick={handleAnalyze} disabled={isAnalyzeDisabled} className="flex-1 h-11" size="lg">
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" aria-hidden="true" />
                  Analyze Document
                </>
              )}
            </Button>

            {analysisResult && (
              <>
                <Button variant="outline" onClick={handleShareToEmail} className="sm:w-auto h-11" size="lg">
                  <Mail className="mr-2 h-4 w-4" aria-hidden="true" />
                  Email Results
                </Button>
                
                <Button variant="outline" onClick={handleReset} className="sm:w-auto h-11 bg-transparent" size="lg">
                  <RotateCcw className="mr-2 h-4 w-4" aria-hidden="true" />
                  New Analysis
                </Button>
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {isLoading && (
        <Card className="shadow-sm">
          <CardContent className="flex items-center justify-center py-12">
            <div className="text-center space-y-4">
              <LoadingSpinner size="lg" className="mx-auto text-primary" />
              <div className="space-y-2">
                <p className="font-medium text-foreground">AI Assembly Line Processing</p>
                <p className="text-sm text-muted-foreground max-w-md">
                  Our multi-agent system is analyzing your document for obligations, rights, and potential red flags...
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {analysisResult && !isLoading && <AnalysisReport result={analysisResult} />}
    </div>
  )
}
