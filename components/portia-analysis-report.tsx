import type { PactGuardAnalysisReport, LegalConcern, BusinessImpact, Recommendation, EmailResponse } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useState } from "react";
import {
  ShieldAlert,
  ShieldCheck,
  ShieldX,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Building,
  Scale,
  Settings,
  Zap,
  Target,
  Calendar,
  Mail,
  Send
} from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

interface AnalysisReportProps {
  result: PactGuardAnalysisReport;
}

const severityConfig: {
  [key: string]: { color: string; textColor: string; icon: React.ElementType };
} = {
  low: { color: "bg-green-500", textColor: "text-green-500", icon: ShieldCheck },
  medium: { color: "bg-yellow-500", textColor: "text-yellow-500", icon: ShieldAlert },
  high: { color: "bg-orange-500", textColor: "text-orange-500", icon: ShieldX },
  critical: { color: "bg-red-600", textColor: "text-red-600", icon: ShieldX },
};

const priorityConfig: {
  [key: string]: { color: string; textColor: string; icon: React.ElementType };
} = {
  immediate: { color: "bg-red-600", textColor: "text-red-600", icon: Zap },
  high: { color: "bg-orange-500", textColor: "text-orange-500", icon: AlertTriangle },
  medium: { color: "bg-yellow-500", textColor: "text-yellow-500", icon: Target },
  low: { color: "bg-green-500", textColor: "text-green-500", icon: CheckCircle },
};

const categoryIcons = {
  financial: DollarSign,
  operational: Building,
  legal: Scale,
  compliance: Settings,
};

const getSeverityBadge = (severity: string) => {
  const config = severityConfig[severity];
  if (!config) return null;
  
  return (
    <Badge
      variant="default"
      className={`text-xs font-semibold text-white ${config.color}`}
    >
      <config.icon className="w-3 h-3 mr-1.5" />
      {severity.toUpperCase()}
    </Badge>
  );
};

const getPriorityBadge = (priority: string) => {
  const config = priorityConfig[priority];
  if (!config) return null;
  
  return (
    <Badge
      variant="default"
      className={`text-xs font-semibold text-white ${config.color}`}
    >
      <config.icon className="w-3 h-3 mr-1.5" />
      {priority.toUpperCase()}
    </Badge>
  );
};

const ReportSection: React.FC<{
  title: string;
  children: React.ReactNode;
}> = ({ title, children }) => (
  <div className="mb-6">
    <h2 className="text-xl font-bold text-foreground mb-4 pb-2 border-b-2 border-primary/20">
      {title}
    </h2>
    {children}
  </div>
);

const LegalConcernCard: React.FC<{ concern: LegalConcern }> = ({ concern }) => {
  const CategoryIcon = categoryIcons[concern.category as keyof typeof categoryIcons] || AlertTriangle;
  
  return (
    <Card className="mb-4 hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <CategoryIcon className="w-5 h-5 text-primary" />
            <CardTitle className="text-base">{concern.title}</CardTitle>
          </div>
          {getSeverityBadge(concern.severity)}
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <p className="text-sm text-muted-foreground">{concern.description}</p>
        <div className="mt-2">
          <Badge variant="outline" className="text-xs">
            {concern.category}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
};

const BusinessImpactCard: React.FC<{ impact: BusinessImpact }> = ({ impact }) => {
  const getSeverityColor = (severity: string) => {
    const colors = {
      critical: "text-red-600 bg-red-50",
      high: "text-orange-600 bg-orange-50",
      medium: "text-yellow-600 bg-yellow-50",
      low: "text-green-600 bg-green-50"
    };
    return colors[severity as keyof typeof colors] || "text-gray-600 bg-gray-50";
  };

  return (
    <Card className="mb-4">
      <CardContent className="pt-4">
        <div className="flex items-start justify-between mb-3">
          <h4 className="font-semibold text-foreground">{impact.category}</h4>
          <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(impact.severity)}`}>
            {impact.severity.toUpperCase()}
          </span>
        </div>
        <p className="text-sm text-muted-foreground mb-2">{impact.impact}</p>
        {impact.financial_exposure && (
          <div className="flex items-center gap-2 text-sm">
            <DollarSign className="w-4 h-4 text-green-600" />
            <span className="text-muted-foreground">Exposure: {impact.financial_exposure}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

const RecommendationCard: React.FC<{ rec: Recommendation }> = ({ rec }) => {
  return (
    <Card className="mb-4">
      <CardContent className="pt-4">
        <div className="flex items-start justify-between mb-3">
          <h4 className="font-semibold text-foreground">{rec.action}</h4>
          {getPriorityBadge(rec.priority)}
        </div>
        <p className="text-sm text-muted-foreground mb-3">{rec.rationale}</p>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>{rec.timeline}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default function PortiaAnalysisReport({ result }: AnalysisReportProps) {
  const [emailRecipient, setEmailRecipient] = useState("");
  const [emailSending, setEmailSending] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);

  const handleSendEmail = async () => {
    if (!emailRecipient.trim()) {
      setEmailError("Please enter a valid email address");
      return;
    }

    setEmailSending(true);
    setEmailError(null);

    try {
      const response = await fetch("/api/send-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          recipient_email: emailRecipient,
          analysis_text: `Legal Analysis Report\n\nDocument Type: ${result.document_type}\nRisk Level: ${result.risk_score.label}\n\nExecutive Summary:\n${result.executive_summary}\n\nGenerated by PactGuard AI Legal Analysis System`,
          subject: `URGENT: Legal Document Risk Alert - ${result.risk_score.label} Risk Detected`
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Unknown error" }));
        throw new Error(errorData.error || "Failed to send email");
      }

      const result_email: EmailResponse = await response.json();
      setEmailSent(true);
      console.log("Email sent successfully:", result_email);
    } catch (err) {
      setEmailError(err instanceof Error ? err.message : "Failed to send email");
    } finally {
      setEmailSending(false);
    }
  };
  return (
    <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
      {/* Header with Risk Score */}
      <Card className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">{result.document_type} Analysis</CardTitle>
              <p className="text-muted-foreground mt-1">
                Analysis completed on {new Date(result.timestamp).toLocaleDateString()}
              </p>
            </div>
            <div className="text-center">
              <div 
                className="w-20 h-20 rounded-full flex items-center justify-center text-2xl font-bold text-white mb-2"
                style={{ backgroundColor: result.risk_score.color }}
              >
                {result.risk_score.level}
              </div>
              <Badge 
                variant="outline" 
                className="bg-white font-semibold"
                style={{ color: result.risk_score.color, borderColor: result.risk_score.color }}
              >
                {result.risk_score.label} Risk
              </Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <h3 className="font-semibold mb-2">Executive Summary</h3>
            <p className="text-muted-foreground">{result.executive_summary}</p>
          </div>
          
          {/* Portia Integration Status */}
          {result.portia_integration && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="font-semibold text-blue-900">Powered by Portia AI + Google Gemini</span>
              </div>
              <div className="text-sm text-blue-700 grid grid-cols-2 gap-4">
                {result.portia_integration.plan_run_id && (
                  <div>Plan Run ID: <code className="bg-blue-100 px-1 rounded">{result.portia_integration.plan_run_id}</code></div>
                )}
                {result.portia_integration.llm_provider && (
                  <div>LLM: {result.portia_integration.llm_provider}</div>
                )}
                {result.portia_integration.billing_generated && (
                  <div className="col-span-2 text-green-700">
                    ✅ Real AI usage generated - check your Portia dashboard!
                  </div>
                )}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Legal Concerns */}
      <ReportSection title={`🚨 Legal Concerns (${result.legal_concerns.length})`}>
        <div className="grid gap-4">
          {result.legal_concerns.map((concern) => (
            <LegalConcernCard key={concern.id} concern={concern} />
          ))}
        </div>
      </ReportSection>

      {/* Business Impact */}
      <ReportSection title={`💼 Business Impact Assessment (${result.business_impact.length})`}>
        <div className="grid gap-4">
          {result.business_impact.map((impact, index) => (
            <BusinessImpactCard key={index} impact={impact} />
          ))}
        </div>
      </ReportSection>

      {/* Recommendations */}
      <ReportSection title={`🎯 Actionable Recommendations (${result.recommendations.length})`}>
        <div className="grid gap-4">
          {result.recommendations.map((rec) => (
            <RecommendationCard key={rec.id} rec={rec} />
          ))}
        </div>
      </ReportSection>

      {/* Gmail Integration Section */}
      <ReportSection title="🔔 Email Alert System">
        <Card className="border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Mail className="h-5 w-5 text-blue-600" />
              Send Legal Alert via Gmail
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Automatically generate and send a professional legal risk alert email using Portia's Gmail integration.
              This will create a draft email with the analysis summary and legal recommendations.
            </p>
            
            {!emailSent ? (
              <div className="space-y-3">
                <div>
                  <label htmlFor="email-recipient" className="block text-sm font-medium mb-1">
                    Recipient Email Address:
                  </label>
                  <input
                    id="email-recipient"
                    type="email"
                    placeholder="legal-team@company.com"
                    value={emailRecipient}
                    onChange={(e) => setEmailRecipient(e.target.value)}
                    className="max-w-md flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  />
                </div>
                
                {emailError && (
                  <div className="text-red-600 text-sm bg-red-50 p-2 rounded">
                    {emailError}
                  </div>
                )}
                
                <Button 
                  onClick={handleSendEmail}
                  disabled={emailSending || !emailRecipient.trim()}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {emailSending ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Sending via Portia Gmail...
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4 mr-2" />
                      Send Legal Alert Email
                    </>
                  )}
                </Button>
                
                <div className="text-xs text-muted-foreground bg-yellow-50 p-2 rounded border border-yellow-200">
                  <strong>Note:</strong> This will use Portia's Gmail tools to create and send an email draft. 
                  The email will include the full legal analysis and risk assessment.
                </div>
              </div>
            ) : (
              <div className="bg-green-50 p-4 rounded border border-green-200">
                <div className="flex items-center gap-2 text-green-800">
                  <CheckCircle className="h-5 w-5" />
                  <strong>Email Sent Successfully!</strong>
                </div>
                <p className="text-green-700 mt-1">
                  Legal alert email has been sent to <strong>{emailRecipient}</strong> via Portia Gmail integration.
                </p>
                <Button 
                  onClick={() => {
                    setEmailSent(false);
                    setEmailRecipient("");
                    setEmailError(null);
                  }}
                  variant="outline"
                  className="mt-3 text-green-800 border-green-300 hover:bg-green-100"
                >
                  Send Another Email
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </ReportSection>

      {/* Footer */}
      <Card className="bg-gray-50">
        <CardContent className="pt-4">
          <div className="text-center text-sm text-muted-foreground">
            <p>Analysis ID: <code>{result.id}</code></p>
            <p className="mt-1">Generated by PactGuard AI Legal Analysis System</p>
            {result.portia_integration.analysis_timestamp && (
              <p className="text-xs mt-1">
                Portia Analysis: {new Date(result.portia_integration.analysis_timestamp).toLocaleString()}
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
