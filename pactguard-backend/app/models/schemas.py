"""
Pydantic models matching the TypeScript interfaces for type safety
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

# Enums for type safety
class DocumentType(str, Enum):
    TERMS_OF_SERVICE = "Terms of Service"
    PRIVACY_POLICY = "Privacy Policy"
    EMPLOYMENT_CONTRACT = "Employment Contract"
    SOFTWARE_LICENSE = "Software License"
    UNKNOWN = "Unknown"

class Sentiment(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class ProcessingStatus(str, Enum):
    COMPLETED = "completed"
    PROCESSING = "processing"
    PENDING = "pending"

# Request Models
class DocumentAnalysisRequest(BaseModel):
    text: str = Field(..., description="The legal document text to analyze")
    url: Optional[str] = Field(None, description="Optional URL of the document")
    document_type: Optional[str] = Field(None, description="Optional document type hint")

# Response Models
class Summary(BaseModel):
    title: str
    documentType: DocumentType
    sentiment: Sentiment
    keyPoints: List[str]
    riskLevel: RiskLevel
    readingTime: str
    lastUpdated: Optional[str] = None

class Obligation(BaseModel):
    id: str
    category: str
    clause: str
    explanation: str
    severity: RiskLevel
    impact: str

class RightAndDataUsage(BaseModel):
    id: str
    category: str
    clause: str
    explanation: str
    severity: RiskLevel
    userProtection: str

class RedFlag(BaseModel):
    id: str
    category: str
    clause: str
    explanation: str
    severity: Literal[RiskLevel.HIGH] = RiskLevel.HIGH  # Red flags are always high severity
    recommendation: str
    legalImplications: str

class ProcessingStep(BaseModel):
    agent: str
    status: ProcessingStatus
    duration: str
    confidence: float = Field(ge=0.0, le=1.0)

class AIAssemblyLine(BaseModel):
    processing_steps: List[ProcessingStep]
    total_processing_time: str

class AnalysisResult(BaseModel):
    summary: Summary
    obligations: List[Obligation]
    rights_and_data_usage: List[RightAndDataUsage]
    red_flags: List[RedFlag]
    ai_assembly_line: AIAssemblyLine

# Internal models for Portia workflow
class DocumentIngestionResult(BaseModel):
    """Result from Document Ingestion Agent"""
    normalized_text: str
    detected_language: str
    word_count: int
    confidence: float

class LegalClassificationResult(BaseModel):
    """Result from Legal Classification Agent"""
    document_type: DocumentType
    confidence: float
    key_sections: List[str]

class ClauseExtractionResult(BaseModel):
    """Result from Clause Extraction Agent"""
    extracted_clauses: List[dict]
    confidence: float

class RiskAnalysisResult(BaseModel):
    """Result from Risk Analysis Agent"""
    obligations: List[Obligation]
    rights_and_data_usage: List[RightAndDataUsage]
    red_flags: List[RedFlag]
    overall_risk: RiskLevel
    confidence: float

class PlainEnglishResult(BaseModel):
    """Result from Plain English Translation Agent"""
    simplified_summary: Summary
    confidence: float

class ReportGenerationResult(BaseModel):
    """Result from Report Generation Agent"""
    final_report: AnalysisResult
    confidence: float
