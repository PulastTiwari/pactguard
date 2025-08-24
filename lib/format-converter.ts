import type { PactGuardAnalysisReport, AnalysisResult } from "../types"

/**
 * Converts the new Portia-integrated backend format to the legacy frontend format
 */
export function convertToLegacyFormat(backendResult: PactGuardAnalysisReport): AnalysisResult {
  return {
    documentType: backendResult.document_type || "Legal Agreement",
    overallRisk: backendResult.risk_score?.label as "Low" | "Medium" | "High" || "Medium",
    summary: {
      overall_risk: backendResult.risk_score?.label as "Low" | "Medium" | "High" || "Medium",
      key_concerns: backendResult.legal_concerns?.map(c => c.title) || [],
      recommendation: backendResult.executive_summary || "Document analysis completed."
    },
    red_flags: backendResult.legal_concerns
      ?.filter(c => c.severity === "high" || c.severity === "critical")
      .map((concern) => ({
        id: concern.id,
        severity: concern.severity === "critical" ? "High" : "Medium" as "Low" | "Medium" | "High",
        title: concern.title,
        explanation: concern.description,
        originalClause: concern.description,
        clause: concern.title
      })) || [],
    obligations: backendResult.recommendations
      ?.filter(r => r.priority === "immediate" || r.priority === "high")
      .map((rec) => ({
        id: rec.id,
        severity: rec.priority === "immediate" ? "High" : "Medium" as "Low" | "Medium" | "High",
        title: rec.action,
        explanation: rec.rationale,
        originalClause: rec.rationale,
        clause: rec.action
      })) || [],
    rights_and_data_usage: backendResult.business_impact
      ?.map((impact, idx) => ({
        id: `impact-${idx}`,
        severity: impact.severity as "Low" | "Medium" | "High" || "Medium",
        title: impact.category,
        explanation: impact.impact,
        originalClause: impact.impact,
        clause: impact.category
      })) || [],
    clauses: backendResult.legal_concerns
      ?.map(concern => ({
        type: concern.severity === "critical" ? "Negative" : 
              concern.severity === "low" ? "Positive" : "Neutral" as "Positive" | "Negative" | "Neutral",
        clause: concern.title,
        explanation: concern.description,
        riskLevel: concern.severity === "critical" ? "High" : 
                   concern.severity === "high" ? "High" :
                   concern.severity === "medium" ? "Medium" : "Low" as "Low" | "Medium" | "High"
      })) || []
  }
}
