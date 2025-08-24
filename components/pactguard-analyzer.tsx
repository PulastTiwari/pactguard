"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Sparkles, RotateCcw, Upload, File, X, Cloud, Search } from "lucide-react"
import { LoadingSpinner } from "@/components/ui/loading-spinner"
import type { PactGuardAnalysisReport } from "@/types"
import PortiaAnalysisReport from "./portia-analysis-report"

// Google OAuth types
declare global {
  interface Window {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string
            scope: string
            callback: (response: GoogleAuthResponse) => void
          }) => {
            requestAccessToken: () => void
          }
        }
      }
    }
  }
}

interface GoogleDriveFile {
  id: string
  name: string
}

interface GoogleAuthResponse {
  access_token: string
  expires_in: number
  token_type: string
}

export default function PactGuardAnalyzer() {
  const [text, setText] = useState("")
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [analysisResult, setAnalysisResult] = useState<PactGuardAnalysisReport | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<"text" | "file" | "drive">("text")
  const [isGoogleAuthenticated, setIsGoogleAuthenticated] = useState(false)
  const [googleAccessToken, setGoogleAccessToken] = useState<string | null>(null)
  const [driveFiles, setDriveFiles] = useState<GoogleDriveFile[]>([])
  const [selectedDriveFile, setSelectedDriveFile] = useState<GoogleDriveFile | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [isSearching, setIsSearching] = useState(false)
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

  const handleGoogleAuth = async () => {
    try {
      // Check if Google API is loaded
      if (typeof window === 'undefined' || !window.google?.accounts?.oauth2) {
        setError('Google OAuth API not loaded. Please refresh the page and try again.')
        return
      }

      // For demo purposes, we'll simulate the Google Drive workflow
      // In production, you would need to set up a proper Google OAuth client ID
      const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID
      
      if (!clientId || clientId === 'your-google-client-id') {
        // Fallback: Simulate authentication for demo
        console.log('Using demo mode for Google Drive integration')
        setIsGoogleAuthenticated(true)
        setGoogleAccessToken('demo-token')
        
        // Show demo files for testing
        setDriveFiles([
          { id: 'demo-1', name: 'Sample Employment Contract.pdf' },
          { id: 'demo-2', name: 'Software License Agreement.docx' },
          { id: 'demo-3', name: 'Terms of Service.txt' },
          { id: 'demo-4', name: 'Privacy Policy.pdf' },
          { id: 'demo-5', name: 'Vendor Agreement.docx' }
        ])
        
        setError(null)
        return
      }

      // Real Google OAuth flow
      const response = await window.google.accounts.oauth2.initTokenClient({
        client_id: clientId,
        scope: 'https://www.googleapis.com/auth/drive.readonly',
        callback: (response: GoogleAuthResponse) => {
          setGoogleAccessToken(response.access_token)
          setIsGoogleAuthenticated(true)
          setError(null)
          console.log('Google authentication successful')
        },
      })
      response.requestAccessToken()
    } catch (error) {
      console.error('Google authentication failed:', error)
      setError('Failed to authenticate with Google. Using demo mode instead.')
      
      // Fallback to demo mode
      setIsGoogleAuthenticated(true)
      setGoogleAccessToken('demo-token')
      setDriveFiles([
        { id: 'demo-1', name: 'Sample Employment Contract.pdf' },
        { id: 'demo-2', name: 'Software License Agreement.docx' },
        { id: 'demo-3', name: 'Terms of Service.txt' }
      ])
    }
  }

  const searchGoogleDrive = async (query: string) => {
    if (!googleAccessToken || !query.trim()) {
      return
    }

    setIsSearching(true)
    try {
      // Demo mode - simulate search results
      if (googleAccessToken === 'demo-token') {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 500))
        
        const allDemoFiles = [
          { id: 'demo-1', name: 'Sample Employment Contract.pdf' },
          { id: 'demo-2', name: 'Software License Agreement.docx' },
          { id: 'demo-3', name: 'Terms of Service.txt' },
          { id: 'demo-4', name: 'Privacy Policy.pdf' },
          { id: 'demo-5', name: 'Vendor Agreement.docx' },
          { id: 'demo-6', name: 'Non-Disclosure Agreement.pdf' },
          { id: 'demo-7', name: 'Service Level Agreement.docx' },
          { id: 'demo-8', name: 'Master Services Agreement.pdf' }
        ]
        
        // Filter demo files based on search query
        const filteredFiles = allDemoFiles.filter(file =>
          file.name.toLowerCase().includes(query.toLowerCase())
        )
        
        setDriveFiles(filteredFiles)
        setIsSearching(false)
        return
      }

      // Real Google Drive API call
      const searchParams = new URLSearchParams({
        q: `name contains '${query}' and (mimeType='application/vnd.google-apps.document' or mimeType='application/pdf' or mimeType='text/plain')`,
        fields: 'files(id,name)',
        pageSize: '10'
      })

      const response = await fetch(`https://www.googleapis.com/drive/v3/files?${searchParams}`, {
        headers: {
          'Authorization': `Bearer ${googleAccessToken}`,
        },
      })

      if (!response.ok) {
        throw new Error('Failed to search Google Drive')
      }

      const data = await response.json()
      setDriveFiles(data.files || [])
    } catch (error) {
      console.error('Google Drive search failed:', error)
      setError('Failed to search Google Drive')
    } finally {
      setIsSearching(false)
    }
  }

  const handleAnalyzeDriveFile = async () => {
    if (!selectedDriveFile) {
      setError("Please select a file from Google Drive")
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch("/api/analyze-drive-file", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file_id: selectedDriveFile.id }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }))
        throw new Error(errorData.error || "Failed to analyze Google Drive file")
      }

      const result: PactGuardAnalysisReport = await response.json()
      setAnalysisResult(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setIsLoading(false)
    }
  }

  const loadDemoContract = () => {
    const demoContract = `SOFTWARE LICENSE AGREEMENT - HIGH RISK DEMO

This Master Enterprise Software Agreement ("Agreement") is entered into effective January 20, 2025, between TechCorp Global Solutions Inc., a Delaware corporation ("Provider") and Customer Enterprise Ltd., a California corporation ("Customer").

1. PAYMENT TERMS AND PENALTIES
Customer must pay all fees within five (5) days of invoice receipt. Late payments incur compound interest at 5% per month (60% annually) plus $1,000 administrative fees. All payments are non-refundable regardless of service performance or termination circumstances. Provider may suspend services immediately upon any payment delay.

2. EXTREME LIMITATION OF LIABILITY  
Provider's total liability is limited to the lesser of $1 or amounts paid by Customer in the preceding 7 days. Provider disclaims ALL warranties express or implied. Provider shall not be liable for ANY damages including direct, indirect, incidental, consequential, punitive, or exemplary damages under any legal theory.

3. COMPREHENSIVE INTELLECTUAL PROPERTY ASSIGNMENT
All intellectual property rights in modifications, customizations, configurations, and data processed through the Software become the exclusive property of Provider. Customer hereby assigns all rights, title, and interest in any work product, including confidential business data and processes, to Provider without compensation.

4. UNILATERAL TERMINATION AND PAYMENT OBLIGATIONS
Provider may terminate immediately without cause or notice. Upon termination by Provider, Customer must continue paying all fees through remaining term and loses all data access. Customer has no right to data return or deletion.

5. UNLIMITED INDEMNIFICATION CLAUSE
Customer agrees to indemnify, defend, and hold harmless Provider from ALL claims, damages, losses, costs, and expenses arising from: (a) Customer's use of Software, (b) Customer's business operations, (c) third-party claims, (d) data breaches, (e) regulatory violations, (f) Provider's negligence, and (g) any other cause whatsoever. This indemnification is unlimited in amount and duration.

This agreement contains multiple extremely high-risk clauses that heavily favor the vendor.`;

    setText(demoContract)
    setActiveTab("text")
    setError(null)
    setAnalysisResult(null)
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
    setSelectedDriveFile(null)
    setSearchQuery("")
    setDriveFiles([])
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const getAnalyzeHandler = () => {
    switch (activeTab) {
      case "text":
        return handleAnalyzeText
      case "file":
        return handleAnalyzeFile
      case "drive":
        return handleAnalyzeDriveFile
      default:
        return handleAnalyzeText
    }
  }

  const getAnalyzeButtonText = () => {
    switch (activeTab) {
      case "text":
        return "Analyze Document"
      case "file":
        return "Analyze File"
      case "drive":
        return "Analyze from Drive"
      default:
        return "Analyze Document"
    }
  }

  const isAnalyzeDisabled = isLoading || 
    (activeTab === "text" && !text.trim()) ||
    (activeTab === "file" && !selectedFile) ||
    (activeTab === "drive" && !selectedDriveFile)

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
            <button
              onClick={() => setActiveTab("drive")}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all flex items-center justify-center ${
                activeTab === "drive"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Cloud className="w-4 h-4 mr-2" />
              Google Drive
            </button>
          </div>

          {/* Text Input Tab */}
          {activeTab === "text" && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label htmlFor="document-text" className="text-sm font-medium text-foreground">
                  Document Text
                </label>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={loadDemoContract}
                  className="text-xs h-7"
                  disabled={isLoading}
                >
                  📋 Load Demo Contract
                </Button>
              </div>
              <Textarea
                id="document-text"
                placeholder="Paste your terms of service, privacy policy, or any legal document here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[200px] resize-none text-sm leading-relaxed"
                disabled={isLoading}
                aria-describedby={error ? "error-message" : undefined}
              />
              {!text && (
                <p className="text-xs text-muted-foreground">
                  💡 Click "Load Demo Contract" to test with a high-risk agreement that will showcase Portia AI analysis
                </p>
              )}
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

          {/* Google Drive Tab */}
          {activeTab === "drive" && (
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Analyze from Google Drive
                </label>
                
                {!isGoogleAuthenticated ? (
                  <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                    <div className="space-y-4">
                      <Cloud className="w-8 h-8 mx-auto text-muted-foreground/60" />
                      <div>
                        <h3 className="text-lg font-medium">Connect to Google Drive</h3>
                        <p className="text-sm text-muted-foreground mt-1">
                          Sign in with Google to search and analyze documents from your Drive
                        </p>
                      </div>
                      <Button
                        onClick={handleGoogleAuth}
                        disabled={isLoading}
                        className="mt-4"
                      >
                        <Cloud className="w-4 h-4 mr-2" />
                        Sign in with Google
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                        <input
                          type="text"
                          placeholder="Search for documents in Google Drive..."
                          value={searchQuery}
                          onChange={(e) => {
                            setSearchQuery(e.target.value)
                            if (e.target.value.trim()) {
                              searchGoogleDrive(e.target.value.trim())
                            } else {
                              setDriveFiles([])
                            }
                          }}
                          className="w-full pl-10 pr-4 py-2 border border-input rounded-md bg-background"
                          disabled={isLoading || isSearching}
                        />
                      </div>
                    </div>

                    {isSearching && (
                      <div className="flex items-center justify-center py-4">
                        <LoadingSpinner size="sm" />
                        <span className="ml-2 text-sm text-muted-foreground">Searching Drive...</span>
                      </div>
                    )}

                    {driveFiles.length > 0 && (
                      <div className="space-y-2">
                        <label className="text-sm font-medium text-foreground">
                          Select a document to analyze:
                        </label>
                        <div className="max-h-60 overflow-y-auto border rounded-md">
                          {driveFiles.map((file) => (
                            <button
                              key={file.id}
                              onClick={() => setSelectedDriveFile(file)}
                              className={`w-full text-left p-3 hover:bg-muted/50 border-b border-border last:border-b-0 transition-colors ${
                                selectedDriveFile?.id === file.id ? 'bg-muted' : ''
                              }`}
                            >
                              <div className="flex items-center space-x-2">
                                <FileText className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                                <span className="text-sm truncate">{file.name}</span>
                                {selectedDriveFile?.id === file.id && (
                                  <span className="text-xs text-primary bg-primary/10 px-2 py-1 rounded">Selected</span>
                                )}
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {searchQuery && driveFiles.length === 0 && !isSearching && (
                      <div className="text-center py-8 text-muted-foreground">
                        <FileText className="w-8 h-8 mx-auto mb-2 opacity-50" />
                        <p>No documents found for "{searchQuery}"</p>
                        <p className="text-xs mt-1">Try searching with different keywords</p>
                      </div>
                    )}
                  </div>
                )}
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
              onClick={getAnalyzeHandler()}
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
                  {getAnalyzeButtonText()}
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

      {analysisResult && !isLoading && <PortiaAnalysisReport result={analysisResult} />}
    </div>
  )
}
