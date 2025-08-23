// Core types for PactGuard legal document analysis

export type Severity = "Low" | "Medium" | "High" | "Critical";

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

export interface PactGuardAnalysisReport {
  summary: AnalysisSummary;
  redFlags: ReportItem[];
  obligations: ReportItem[];
  rightsAndDataUsage: ReportItem[];
}

// This is the legacy type, we'll keep it for now to avoid breaking the mock API immediately
// and will transition to the new type.
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
