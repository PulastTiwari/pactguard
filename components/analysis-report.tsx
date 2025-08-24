import type { AnalysisResult, Severity } from "@/types"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { AlertTriangle, Shield, FileText, Flag } from "lucide-react"

interface AnalysisReportProps {
  result: AnalysisResult
}

function getSeverityVariant(severity: Severity): "default" | "secondary" | "destructive" {
  switch (severity) {
    case "Low":
      return "secondary"
    case "Medium":
      return "default"
    case "High":
      return "destructive"
    default:
      return "default"
  }
}

function getSeverityColor(severity: Severity): string {
  switch (severity) {
    case "Low":
      return "text-emerald-700 dark:text-emerald-300"
    case "Medium":
      return "text-amber-700 dark:text-amber-300"
    case "High":
      return "text-red-700 dark:text-red-300"
    default:
      return "text-slate-600 dark:text-slate-400"
  }
}

export default function AnalysisReport({ result }: AnalysisReportProps) {
  return (
    <div className="space-y-6" role="main" aria-label="Document analysis results">
      {/* Summary Card */}
      <Card className="border-l-4 border-l-primary shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <Shield className="h-5 w-5 text-primary" aria-hidden="true" />
            <CardTitle className="text-lg font-semibold">Analysis Summary</CardTitle>
          </div>
          <CardDescription className="flex items-center gap-2 text-base">
            Overall Risk Level:
            <Badge
              variant={getSeverityVariant(result.summary.overall_risk)}
              className="text-sm font-medium"
              aria-label={`Risk level: ${result.summary.overall_risk}`}
            >
              {result.summary.overall_risk}
            </Badge>
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <h3 className="font-semibold mb-3 text-foreground">Key Concerns:</h3>
            <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground pl-2">
              {result.summary.key_concerns.map((concern, index) => (
                <li key={index} className="leading-relaxed">
                  {concern}
                </li>
              ))}
            </ul>
          </div>
          <div className="p-4 bg-muted/50 rounded-lg border">
            <h4 className="text-sm font-semibold text-foreground mb-2">Recommendation:</h4>
            <p className="text-sm text-muted-foreground leading-relaxed">{result.summary.recommendation}</p>
          </div>
        </CardContent>
      </Card>

      {/* Red Flags */}
      {result.red_flags.length > 0 && (
        <Card className="border-l-4 border-l-destructive shadow-sm">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Flag className="h-5 w-5 text-destructive" aria-hidden="true" />
              <CardTitle className="text-lg font-semibold text-destructive">Red Flags</CardTitle>
            </div>
            <CardDescription>Critical issues that require immediate attention</CardDescription>
          </CardHeader>
          <CardContent>
            <Accordion type="single" collapsible className="w-full">
              {result.red_flags.map((flag) => (
                <AccordionItem key={flag.id} value={flag.id} className="border-b border-border/50">
                  <AccordionTrigger className="text-left hover:no-underline py-4">
                    <div className="flex items-center justify-between w-full mr-4 gap-3">
                      <span className="text-sm font-medium text-foreground leading-relaxed flex-1 text-left">
                        {flag.clause}
                      </span>
                      <Badge variant={getSeverityVariant(flag.severity)} className="shrink-0">
                        {flag.severity}
                      </Badge>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="pb-4">
                    <p className="text-sm text-muted-foreground leading-relaxed pl-1">{flag.explanation}</p>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </CardContent>
        </Card>
      )}

      {/* Obligations */}
      <Card className="shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <FileText className="h-5 w-5 text-primary" aria-hidden="true" />
            <CardTitle className="text-lg font-semibold">Your Obligations</CardTitle>
          </div>
          <CardDescription>What you agree to do by accepting this document</CardDescription>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="w-full">
            {result.obligations.map((obligation) => (
              <AccordionItem key={obligation.id} value={obligation.id} className="border-b border-border/50">
                <AccordionTrigger className="text-left hover:no-underline py-4">
                  <div className="flex items-center justify-between w-full mr-4 gap-3">
                    <span className="text-sm font-medium text-foreground leading-relaxed flex-1 text-left">
                      {obligation.clause}
                    </span>
                    <Badge variant={getSeverityVariant(obligation.severity)} className="shrink-0">
                      {obligation.severity}
                    </Badge>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pb-4">
                  <p className="text-sm text-muted-foreground leading-relaxed pl-1">{obligation.explanation}</p>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </CardContent>
      </Card>

      {/* Rights and Data Usage */}
      <Card className="shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <AlertTriangle className="h-5 w-5 text-primary" aria-hidden="true" />
            <CardTitle className="text-lg font-semibold">Rights & Data Usage</CardTitle>
          </div>
          <CardDescription>How your data will be collected and used</CardDescription>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="w-full">
            {result.rights_and_data_usage.map((right) => (
              <AccordionItem key={right.id} value={right.id} className="border-b border-border/50">
                <AccordionTrigger className="text-left hover:no-underline py-4">
                  <div className="flex items-center justify-between w-full mr-4 gap-3">
                    <span className="text-sm font-medium text-foreground leading-relaxed flex-1 text-left">
                      {right.clause}
                    </span>
                    <Badge variant={getSeverityVariant(right.severity)} className="shrink-0">
                      {right.severity}
                    </Badge>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pb-4">
                  <p className="text-sm text-muted-foreground leading-relaxed pl-1">{right.explanation}</p>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </CardContent>
      </Card>
    </div>
  )
}
