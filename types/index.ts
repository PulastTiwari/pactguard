// Core types for PactGuard legal document analysis

export type Severity = "Low" | "Medium" | "High" | "Critical";

// New Portia-integrated types
export interface RiskLevel {
  level: number;  // 1-10 scale
  label: string;  // "Low", "Medium", "High", "Critical"
  color: string;  // hex color code
}

export interface LegalConcern {
  id: string;
  title: string;
  description: string;
  severity: "low" | "medium" | "high" | "critical";
  category: "financial" | "operational" | "legal" | "compliance";
}

export interface BusinessImpact {
  category: string;
  impact: string;
  severity: string;
  financial_exposure?: string;
}

export interface Recommendation {
  id: string;
  priority: "immediate" | "high" | "medium" | "low";
  action: string;
  rationale: string;
  timeline: string;
}

export interface PortiaIntegration {
  status: string;
  plan_run_id?: string;
  llm_provider?: string;
  analysis_timestamp?: string;
  portia_used?: boolean;
  billing_generated?: boolean;
}

// Gmail integration types
export interface EmailRequest {
  recipient_email: string;
  analysis_text: string;
  subject?: string;
}

export interface EmailResponse {
  success: boolean;
  recipient: string;
  subject: string;
  gmail_integration: any;
  timestamp: string;
  message: string;
}

// Main analysis report structure (Portia-integrated)
export interface PactGuardAnalysisReport {
  id: string;
  timestamp: string;
  document_type: string;
  risk_score: RiskLevel;
  executive_summary: string;
  legal_concerns: LegalConcern[];
  business_impact: BusinessImpact[];
  recommendations: Recommendation[];
  portia_integration: PortiaIntegration;
}

// Legacy types for backwards compatibility
export interface AnalysisSummary {
  documentType: string;
  overallRiskLevel: Severity;
  keyConcerns: string[];
  recommendation: string;
}

export interface ReportItem {
  severity: Severity;
  title: string;
  explanation: string;
  originalClause: string;
}

export interface LegacyAnalysisReport {
  summary: AnalysisSummary;
  redFlags: ReportItem[];
  obligations: ReportItem[];
  rightsAndDataUsage: ReportItem[];
}

export interface AnalysisResult {
  documentType: string;
  overallRisk: "Low" | "Medium" | "High";
  summary: string;
  clauses: {
    type: "Positive" | "Negative" | "Neutral";
    clause: string;
    explanation: string;
    riskLevel: "Low" | "Medium" | "High";
  }[];
}
