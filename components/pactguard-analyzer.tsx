"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Sparkles, RotateCcw, Upload, File, X } from "lucide-react"
import { LoadingSpinner } from "@/components/ui/loading-spinner"
import type { PactGuardAnalysisReport } from "@/types"
import AnalysisReport from "./analysis-report"

export default function PactGuardAnalyzer() {
  const [text, setText] = useState("")
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [analysisResult, setAnalysisResult] = useState<PactGuardAnalysisReport | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<"text" | "file">("text")
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleAnalyzeText = async () => {
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
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }))
        throw new Error(errorData.error || "Failed to analyze document")
      }

      const result: PactGuardAnalysisReport = await response.json()
      setAnalysisResult(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  const handleAnalyzeFile = async () => {
    if (!selectedFile) {
      setError("Please select a file to analyze")
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append("file", selectedFile)

      const response = await fetch("/api/analyze-file", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }))
        throw new Error(errorData.error || "Failed to analyze file")
      }

      const result: PactGuardAnalysisReport = await response.json()
      setAnalysisResult(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
      const isValidType = allowedTypes.includes(file.type) || 
                         file.name.endsWith('.pdf') || 
                         file.name.endsWith('.docx') || 
                         file.name.endsWith('.txt')
      
      if (!isValidType) {
        setError("Please select a PDF, DOCX, or TXT file")
        return
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB")
        return
      }

      setSelectedFile(file)
      setError(null)
    }
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const handleReset = () => {
    setText("")
    setSelectedFile(null)
    setAnalysisResult(null)
    setError(null)
    setActiveTab("text")
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const isAnalyzeDisabled = isLoading || (activeTab === "text" ? !text.trim() : !selectedFile)

  return (
    <div className="space-y-6">
      <Card className="shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <FileText className="h-6 w-6 text-primary" aria-hidden="true" />
            <div>
              <CardTitle className="text-xl font-semibold">Document Analyzer</CardTitle>
              <CardDescription className="mt-1">
                Upload a document or paste text below to get an AI-powered legal analysis
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Tab Selection */}
          <div className="flex space-x-1 p-1 bg-muted rounded-lg">
            <button
              onClick={() => setActiveTab("text")}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all flex items-center justify-center ${
                activeTab === "text"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <FileText className="w-4 h-4 mr-2" />
              Text Input
            </button>
            <button
              onClick={() => setActiveTab("file")}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all flex items-center justify-center ${
                activeTab === "file"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Upload className="w-4 h-4 mr-2" />
              File Upload
            </button>
          </div>

          {/* Text Input Tab */}
          {activeTab === "text" && (
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
          )}

          {/* File Upload Tab */}
          {activeTab === "file" && (
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Upload Document
                </label>
                <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center hover:border-muted-foreground/40 transition-colors">
                  {selectedFile ? (
                    <div className="space-y-4">
                      <div className="flex items-center justify-center space-x-2 text-sm text-muted-foreground">
                        <File className="w-4 h-4" />
                        <span>{selectedFile.name}</span>
                        <span>({(selectedFile.size / 1024).toFixed(1)} KB)</span>
                        <button
                          onClick={handleRemoveFile}
                          className="ml-2 text-destructive hover:text-destructive/80"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <Upload className="w-8 h-8 mx-auto text-muted-foreground/60" />
                      <div>
                        <Button
                          variant="outline"
                          onClick={() => fileInputRef.current?.click()}
                          disabled={isLoading}
                        >
                          Choose File
                        </Button>
                        <p className="mt-2 text-xs text-muted-foreground">
                          Supported formats: PDF, DOCX, TXT (max 10MB)
                        </p>
                      </div>
                    </div>
                  )}
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileSelect}
                    className="hidden"
                    disabled={isLoading}
                  />
                </div>
              </div>
            </div>
          )}

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
            <Button 
              onClick={activeTab === "text" ? handleAnalyzeText : handleAnalyzeFile}
              disabled={isAnalyzeDisabled} 
              className="flex-1 h-11" 
              size="lg"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" aria-hidden="true" />
                  Analyze {activeTab === "text" ? "Document" : "File"}
                </>
              )}
            </Button>

            {analysisResult && (
              <Button variant="outline" onClick={handleReset} className="sm:w-auto h-11 bg-transparent" size="lg">
                <RotateCcw className="mr-2 h-4 w-4" aria-hidden="true" />
                New Analysis
              </Button>
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
