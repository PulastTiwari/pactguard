"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FileUp, Mail, FolderOpen, Activity, Upload, Send } from "lucide-react"
import { LoadingSpinner } from "@/components/ui/loading-spinner"
import { Alert, AlertDescription } from "@/components/ui/alert"
import type { AnalysisResult, EmailRequest } from "@/types"
import AnalysisReport from "./analysis-report"
import { AnalysisSharing } from "@/lib/analysis-sharing"

interface DemoStatus {
  portia_client_initialized: boolean
  api_keys_configured: {
    portia_api_key_present: boolean
    google_api_key_present: boolean
  }
  portia_sdk_available: boolean
  demo_ready: boolean
}

export default function AdvancedFeatures() {
  const [activeTab, setActiveTab] = useState("upload")
  
  // File Upload State
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isFileAnalyzing, setIsFileAnalyzing] = useState(false)
  const [fileAnalysisResult, setFileAnalysisResult] = useState<AnalysisResult | null>(null)
  const [fileError, setFileError] = useState<string | null>(null)

  // Google Drive State  
  const [driveFileId, setDriveFileId] = useState("")
  const [isDriveAnalyzing, setIsDriveAnalyzing] = useState(false)
  const [driveAnalysisResult, setDriveAnalysisResult] = useState<AnalysisResult | null>(null)
  const [driveError, setDriveError] = useState<string | null>(null)

  // Email State
  const [recipientEmail, setRecipientEmail] = useState("")
  const [emailSubject, setEmailSubject] = useState("Legal Document Risk Alert - PactGuard Analysis")
  const [analysisToEmail, setAnalysisToEmail] = useState<AnalysisResult | null>(null)
  const [isEmailSending, setIsEmailSending] = useState(false)
  const [emailSuccess, setEmailSuccess] = useState<string | null>(null)
  const [emailError, setEmailError] = useState<string | null>(null)

  // Demo Status State
  const [demoStatus, setDemoStatus] = useState<DemoStatus | null>(null)
  const [isLoadingStatus, setIsLoadingStatus] = useState(false)

  // Listen for shared analysis from other components
  useEffect(() => {
    const cleanup = AnalysisSharing.getInstance().onAnalysisShared((sharedAnalysis) => {
      setAnalysisToEmail(sharedAnalysis)
      setActiveTab("email") // Switch to email tab when analysis is shared
    })

    // Check for existing shared analysis
    const existingAnalysis = AnalysisSharing.getInstance().getLatestAnalysis()
    if (existingAnalysis && !analysisToEmail) {
      setAnalysisToEmail(existingAnalysis)
    }

    return cleanup
  }, [])

  // File Upload Handler
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setSelectedFile(file)
    setFileError(null)
    setFileAnalysisResult(null)
  }

  const analyzeFile = async () => {
    if (!selectedFile) {
      setFileError("Please select a file first")
      return
    }

    setIsFileAnalyzing(true)
    setFileError(null)

    try {
      const formData = new FormData()
      formData.append("file", selectedFile)

      const response = await fetch("/api/analyze-file", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Failed to analyze file")
      }

      const result: AnalysisResult = await response.json()
      setFileAnalysisResult(result)
    } catch (err) {
      setFileError(err instanceof Error ? err.message : "File analysis failed")
    } finally {
      setIsFileAnalyzing(false)
    }
  }

  // Google Drive Analysis Handler
  const analyzeDriveFile = async () => {
    if (!driveFileId.trim()) {
      setDriveError("Please enter a Google Drive file ID")
      return
    }

    setIsDriveAnalyzing(true)
    setDriveError(null)
    setDriveAnalysisResult(null)

    try {
      const response = await fetch("/api/analyze-drive-file", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file_id: driveFileId }),
      })

      if (!response.ok) {
        throw new Error("Failed to analyze Google Drive file")
      }

      const result: AnalysisResult = await response.json()
      setDriveAnalysisResult(result)
    } catch (err) {
      setDriveError(err instanceof Error ? err.message : "Google Drive analysis failed")
    } finally {
      setIsDriveAnalyzing(false)
    }
  }

  // Email Sending Handler
  const sendAnalysisEmail = async () => {
    if (!recipientEmail.trim()) {
      setEmailError("Please enter recipient email")
      return
    }

    if (!analysisToEmail) {
      setEmailError("No analysis available to send")
      return
    }

    setIsEmailSending(true)
    setEmailError(null)
    setEmailSuccess(null)

    try {
      const emailData: EmailRequest = {
        recipient_email: recipientEmail,
        analysis_text: `Analysis Report: ${analysisToEmail.summary.recommendation}. Key concerns: ${analysisToEmail.summary.key_concerns.join(', ')}`,
        subject: emailSubject
      }

      const response = await fetch("/api/send-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(emailData),
      })

      if (!response.ok) {
        throw new Error("Failed to send email")
      }

      const result = await response.json()
      setEmailSuccess("Analysis email sent successfully!")
      setRecipientEmail("")
    } catch (err) {
      setEmailError(err instanceof Error ? err.message : "Failed to send email")
    } finally {
      setIsEmailSending(false)
    }
  }

  // Demo Status Handler
  const checkDemoStatus = async () => {
    setIsLoadingStatus(true)

    try {
      const response = await fetch("http://localhost:8000/demo-status")
      
      if (!response.ok) {
        throw new Error("Failed to fetch demo status")
      }

      const status: DemoStatus = await response.json()
      setDemoStatus(status)
    } catch (err) {
      console.error("Demo status check failed:", err)
    } finally {
      setIsLoadingStatus(false)
    }
  }

  return (
    <Card className="shadow-sm">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Advanced Analysis Features</CardTitle>
        <CardDescription>
          Upload files, analyze Google Drive documents, send results via email, and check system status
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid grid-cols-4 w-full">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <FileUp className="h-4 w-4" />
              Upload
            </TabsTrigger>
            <TabsTrigger value="drive" className="flex items-center gap-2">
              <FolderOpen className="h-4 w-4" />
              Drive
            </TabsTrigger>
            <TabsTrigger value="email" className="flex items-center gap-2">
              <Mail className="h-4 w-4" />
              Email
            </TabsTrigger>
            <TabsTrigger value="status" className="flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Status
            </TabsTrigger>
          </TabsList>

          {/* File Upload Tab */}
          <TabsContent value="upload" className="space-y-6">
            <div className="space-y-4">
              <Label htmlFor="file-upload" className="text-sm font-medium">
                Upload Document File
              </Label>
              <div className="flex items-center gap-4">
                <Input
                  id="file-upload"
                  type="file"
                  accept=".txt,.pdf,.doc,.docx"
                  onChange={handleFileUpload}
                  disabled={isFileAnalyzing}
                  className="cursor-pointer"
                />
                <Button
                  onClick={analyzeFile}
                  disabled={!selectedFile || isFileAnalyzing}
                  className="flex items-center gap-2"
                >
                  {isFileAnalyzing ? (
                    <>
                      <LoadingSpinner size="sm" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Upload className="h-4 w-4" />
                      Analyze File
                    </>
                  )}
                </Button>
              </div>

              {selectedFile && (
                <p className="text-sm text-muted-foreground">
                  Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                </p>
              )}

              {fileError && (
                <Alert variant="destructive">
                  <AlertDescription>{fileError}</AlertDescription>
                </Alert>
              )}

              {fileAnalysisResult && <AnalysisReport result={fileAnalysisResult} />}
            </div>
          </TabsContent>

          {/* Google Drive Tab */}
          <TabsContent value="drive" className="space-y-6">
            <div className="space-y-4">
              <Label htmlFor="drive-file-id" className="text-sm font-medium">
                Google Drive File ID
              </Label>
              <div className="flex items-center gap-4">
                <Input
                  id="drive-file-id"
                  placeholder="Enter Google Drive file ID (e.g., 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms)"
                  value={driveFileId}
                  onChange={(e) => setDriveFileId(e.target.value)}
                  disabled={isDriveAnalyzing}
                />
                <Button
                  onClick={analyzeDriveFile}
                  disabled={!driveFileId.trim() || isDriveAnalyzing}
                  className="flex items-center gap-2"
                >
                  {isDriveAnalyzing ? (
                    <>
                      <LoadingSpinner size="sm" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <FolderOpen className="h-4 w-4" />
                      Analyze
                    </>
                  )}
                </Button>
              </div>

              <p className="text-xs text-muted-foreground">
                Find the file ID in the Google Drive URL: https://docs.google.com/document/d/YOUR_FILE_ID/edit
              </p>

              {driveError && (
                <Alert variant="destructive">
                  <AlertDescription>{driveError}</AlertDescription>
                </Alert>
              )}

              {driveAnalysisResult && (
                <div className="space-y-4">
                  <Button
                    onClick={() => setAnalysisToEmail(driveAnalysisResult)}
                    variant="outline"
                    size="sm"
                    className="flex items-center gap-2"
                  >
                    <Mail className="h-4 w-4" />
                    Prepare for Email
                  </Button>
                  <AnalysisReport result={driveAnalysisResult} />
                </div>
              )}
            </div>
          </TabsContent>

          {/* Email Tab */}
          <TabsContent value="email" className="space-y-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="recipient-email">Recipient Email</Label>
                <Input
                  id="recipient-email"
                  type="email"
                  placeholder="recipient@example.com"
                  value={recipientEmail}
                  onChange={(e) => setRecipientEmail(e.target.value)}
                  disabled={isEmailSending}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email-subject">Email Subject</Label>
                <Input
                  id="email-subject"
                  value={emailSubject}
                  onChange={(e) => setEmailSubject(e.target.value)}
                  disabled={isEmailSending}
                />
              </div>

              {!analysisToEmail && (
                <Alert>
                  <AlertDescription>
                    No analysis selected. Analyze a document first or use the "Prepare for Email" button.
                  </AlertDescription>
                </Alert>
              )}

              <Button
                onClick={sendAnalysisEmail}
                disabled={!recipientEmail.trim() || !analysisToEmail || isEmailSending}
                className="flex items-center gap-2"
              >
                {isEmailSending ? (
                  <>
                    <LoadingSpinner size="sm" />
                    Sending...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    Send Analysis Email
                  </>
                )}
              </Button>

              {emailSuccess && (
                <Alert>
                  <AlertDescription className="text-green-600">{emailSuccess}</AlertDescription>
                </Alert>
              )}

              {emailError && (
                <Alert variant="destructive">
                  <AlertDescription>{emailError}</AlertDescription>
                </Alert>
              )}
            </div>
          </TabsContent>

          {/* System Status Tab */}
          <TabsContent value="status" className="space-y-6">
            <div className="space-y-4">
              <Button
                onClick={checkDemoStatus}
                disabled={isLoadingStatus}
                className="flex items-center gap-2"
              >
                {isLoadingStatus ? (
                  <>
                    <LoadingSpinner size="sm" />
                    Checking...
                  </>
                ) : (
                  <>
                    <Activity className="h-4 w-4" />
                    Check System Status
                  </>
                )}
              </Button>

              {demoStatus && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card className={demoStatus.demo_ready ? "border-green-500" : "border-yellow-500"}>
                    <CardContent className="pt-6">
                      <h4 className="font-medium mb-2">System Status</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Demo Ready:</span>
                          <span className={demoStatus.demo_ready ? "text-green-600" : "text-yellow-600"}>
                            {demoStatus.demo_ready ? "✅ Yes" : "⚠️ Issues"}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Portia Client:</span>
                          <span className={demoStatus.portia_client_initialized ? "text-green-600" : "text-red-600"}>
                            {demoStatus.portia_client_initialized ? "✅ Active" : "❌ Inactive"}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>SDK Available:</span>
                          <span className={demoStatus.portia_sdk_available ? "text-green-600" : "text-red-600"}>
                            {demoStatus.portia_sdk_available ? "✅ Yes" : "❌ No"}
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="pt-6">
                      <h4 className="font-medium mb-2">API Configuration</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Portia API Key:</span>
                          <span className={demoStatus.api_keys_configured.portia_api_key_present ? "text-green-600" : "text-red-600"}>
                            {demoStatus.api_keys_configured.portia_api_key_present ? "✅ Set" : "❌ Missing"}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Google API Key:</span>
                          <span className={demoStatus.api_keys_configured.google_api_key_present ? "text-green-600" : "text-red-600"}>
                            {demoStatus.api_keys_configured.google_api_key_present ? "✅ Set" : "❌ Missing"}
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
