"""
Custom Portia Tools for PactGuard AI Assembly Line

Each tool represents a specialized agent in the document analysis workflow.
"""
import re
import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from portia import Tool, ToolRunContext, ToolHardError

from app.models.schemas import (
    AnalysisResult, DocumentIngestionResult, LegalClassificationResult, ClauseExtractionResult,
    RiskAnalysisResult, PlainEnglishResult, ReportGenerationResult,
    DocumentType, RiskLevel, Sentiment, Summary, ProcessingStep, AIAssemblyLine,
    Obligation, RightAndDataUsage, RedFlag
)

# --- Argument Schemas for Tools ---

class DocumentIngestionArgs(BaseModel):
    document_text: str = Field(description="The raw legal document text to normalize")

class LegalClassificationArgs(BaseModel):
    normalized_text: str = Field(description="The normalized document text to classify")

class ClauseExtractionArgs(BaseModel):
    normalized_text: str = Field(description="The normalized document text")
    document_type: DocumentType = Field(description="The classified document type")
    key_sections: List[str] = Field(description="The identified key sections")

class RiskAnalysisArgs(BaseModel):
    extracted_clauses: List[dict] = Field(description="The extracted legal clauses")

class PlainEnglishTranslationArgs(BaseModel):
    document_type: DocumentType = Field(description="The document type")
    overall_risk: RiskLevel = Field(description="The overall risk level")
    word_count: int = Field(description="The document word count")

class ReportGenerationArgs(BaseModel):
    summary: Summary = Field(description="The plain English summary")
    obligations: List[Obligation] = Field(description="The user obligations")
    rights_and_data_usage: List[RightAndDataUsage] = Field(description="The rights and data usage items")
    red_flags: List[RedFlag] = Field(description="The red flags")
    processing_steps: List[ProcessingStep] = Field(description="The AI assembly line processing steps")


# --- Tool Definitions ---

class DocumentIngestionTool(Tool[DocumentIngestionResult]):
    """Agent 1: Document Ingestion - Normalizes and prepares document content"""
    
    id: str = "document_ingestion"
    name: str = "Document Ingestion"
    description: str = "Normalizes and prepares legal document content for analysis"
    args_schema: type[BaseModel] = DocumentIngestionArgs
    output_schema: tuple[str, str] = ("DocumentIngestionResult", "Normalized text and metadata")

    def run(self, context: ToolRunContext, document_text: str) -> DocumentIngestionResult:
        try:
            normalized_text = self._normalize_text(document_text)
            word_count = len(normalized_text.split())
            
            return DocumentIngestionResult(
                normalized_text=normalized_text,
                detected_language="English",
                word_count=word_count,
                confidence=0.95
            )
        except Exception as e:
            raise ToolHardError(f"Document ingestion failed: {str(e)}") from e
    
    def _normalize_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text.strip())
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        return text

class LegalClassificationTool(Tool[LegalClassificationResult]):
    """Agent 2: Legal Classification - Identifies document type and structure"""
    
    id: str = "legal_classification"
    name: str = "Legal Classification"
    description: str = "Classifies the type of legal document and identifies key sections"
    args_schema: type[BaseModel] = LegalClassificationArgs
    output_schema: tuple[str, str] = ("LegalClassificationResult", "Document type and key sections")

    def run(self, context: ToolRunContext, normalized_text: str) -> LegalClassificationResult:
        try:
            document_type = self._classify_document_type(normalized_text)
            key_sections = self._identify_key_sections(normalized_text, document_type)
            
            return LegalClassificationResult(
                document_type=document_type,
                confidence=0.92,
                key_sections=key_sections
            )
        except Exception as e:
            raise ToolHardError(f"Legal classification failed: {str(e)}") from e
    
    def _classify_document_type(self, text: str) -> DocumentType:
        text_lower = text.lower()
        if any(k in text_lower for k in ["terms of service", "terms of use"]):
            return DocumentType.TERMS_OF_SERVICE
        if any(k in text_lower for k in ["privacy policy", "data collection"]):
            return DocumentType.PRIVACY_POLICY
        if any(k in text_lower for k in ["employment agreement", "employment contract"]):
            return DocumentType.EMPLOYMENT_CONTRACT
        if any(k in text_lower for k in ["software license", "mit license"]):
            return DocumentType.SOFTWARE_LICENSE
        return DocumentType.UNKNOWN
    
    def _identify_key_sections(self, text: str, doc_type: DocumentType) -> List[str]:
        if doc_type == DocumentType.PRIVACY_POLICY:
            return ["Data Collection", "Data Usage", "Data Sharing", "User Rights", "Cookies"]
        if doc_type == DocumentType.TERMS_OF_SERVICE:
            return ["User Obligations", "Service Terms", "Liability", "Termination", "Dispute Resolution"]
        return ["General Terms", "Conditions", "Rights", "Obligations"]

class ClauseExtractionTool(Tool[ClauseExtractionResult]):
    """Agent 3: Clause Extraction - Identifies and extracts specific legal clauses"""
    
    id: str = "clause_extraction"
    name: str = "Clause Extraction"
    description: str = "Extracts and identifies specific legal clauses from the document"
    args_schema: type[BaseModel] = ClauseExtractionArgs
    output_schema: tuple[str, str] = ("ClauseExtractionResult", "List of extracted clauses")

    def run(self, context: ToolRunContext, normalized_text: str, document_type: DocumentType, key_sections: List[str]) -> ClauseExtractionResult:
        try:
            extracted_clauses = self._extract_clauses(normalized_text, key_sections)
            return ClauseExtractionResult(
                extracted_clauses=extracted_clauses,
                confidence=0.89
            )
        except Exception as e:
            raise ToolHardError(f"Clause extraction failed: {str(e)}") from e
    
    def _extract_clauses(self, text: str, sections: List[str]) -> List[dict]:
        clauses = []
        sentences = text.split('. ')
        keywords = {
            "risk": ["liable", "responsibility", "terminate", "breach", "penalty"],
            "data_usage": ["collect", "store", "share", "process", "personal data"],
            "obligation": ["must", "shall", "required", "agree to", "consent"]
        }
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            clause_type = "general"
            for type, kws in keywords.items():
                if any(kw in sentence_lower for kw in kws):
                    clause_type = type
                    break
            
            clauses.append({
                "id": str(uuid.uuid4()),
                "text": sentence.strip(),
                "section": self._classify_clause_section(sentence_lower, sections),
                "type": clause_type
            })
        return clauses[:20]

    def _classify_clause_section(self, text: str, sections: List[str]) -> str:
        for section in sections:
            if any(word in text for word in section.lower().split()):
                return section
        return "General Terms"

class RiskAnalysisTool(Tool[RiskAnalysisResult]):
    """Agent 4: Risk Analysis - Analyzes legal risks and assigns severity scores"""
    
    id: str = "risk_analysis" 
    name: str = "Risk Analysis"
    description: str = "Analyzes legal risks and categorizes clauses by severity"
    args_schema: type[BaseModel] = RiskAnalysisArgs
    output_schema: tuple[str, str] = ("RiskAnalysisResult", "Categorized risks and overall assessment")

    def run(self, context: ToolRunContext, extracted_clauses: List[dict]) -> RiskAnalysisResult:
        try:
            obligations, rights, red_flags = [], [], []
            for clause in extracted_clauses:
                if clause["type"] == "obligation":
                    obligations.append(Obligation(**self._create_item(clause, "obligation")))
                elif clause["type"] == "data_usage":
                    rights.append(RightAndDataUsage(**self._create_item(clause, "data_usage")))
                elif clause["type"] == "risk":
                    red_flags.append(RedFlag(**self._create_item(clause, "red_flag")))
            
            overall_risk = self._calculate_overall_risk(red_flags)
            
            return RiskAnalysisResult(
                obligations=obligations,
                rights_and_data_usage=rights,
                red_flags=red_flags,
                overall_risk=overall_risk,
                confidence=0.87
            )
        except Exception as e:
            raise ToolHardError(f"Risk analysis failed: {str(e)}") from e
    
    def _create_item(self, clause: dict, item_type: str) -> dict:
        item = {
            "id": clause["id"],
            "category": clause["section"],
            "clause": clause["text"][:200],
            "explanation": f"This clause defines a key {item_type.replace('_', ' ')}.",
            "severity": RiskLevel.MEDIUM,
        }
        if item_type == "obligation":
            item["impact"] = "User must comply with this."
        elif item_type == "data_usage":
            item["userProtection"] = "Affects user data and privacy."
        elif item_type == "red_flag":
            item.update({
                "severity": RiskLevel.HIGH,
                "recommendation": "Review this clause carefully.",
                "legalImplications": "Potential for significant legal consequences."
            })
        return item
    
    def _calculate_overall_risk(self, red_flags: List) -> RiskLevel:
        if red_flags:
            return RiskLevel.HIGH
        elif len(red_flags) > 0:
             return RiskLevel.MEDIUM
        return RiskLevel.LOW

class PlainEnglishTranslationTool(Tool[PlainEnglishResult]):
    """Agent 5: Plain English Translation - Converts legal jargon to simple language"""
    
    id: str = "plain_english_translation"
    name: str = "Plain English Translation"
    description: str = "Translates legal jargon into plain English summaries"
    args_schema: type[BaseModel] = PlainEnglishTranslationArgs
    output_schema: tuple[str, str] = ("PlainEnglishResult", "A simplified summary of the document")

    def run(self, context: ToolRunContext, document_type: DocumentType, overall_risk: RiskLevel, word_count: int) -> PlainEnglishResult:
        try:
            reading_time = f"{max(1, word_count // 200)} min read"
            
            sentiment = Sentiment.NEUTRAL
            if overall_risk == RiskLevel.HIGH:
                sentiment = Sentiment.NEGATIVE
            elif overall_risk == RiskLevel.LOW:
                sentiment = Sentiment.POSITIVE

            summary = Summary(
                title=f"Legal Document Analysis: {document_type.value}",
                documentType=document_type,
                sentiment=sentiment,
                keyPoints=self._generate_key_points(document_type),
                riskLevel=overall_risk,
                readingTime=reading_time,
                lastUpdated=datetime.now().isoformat()
            )
            return PlainEnglishResult(simplified_summary=summary, confidence=0.91)
        except Exception as e:
            raise ToolHardError(f"Plain english translation failed: {str(e)}") from e
    
    def _generate_key_points(self, doc_type: DocumentType) -> List[str]:
        points = {
            DocumentType.PRIVACY_POLICY: [
                "Explains how your personal data is collected and used.",
                "Describes data sharing practices with third parties.", 
                "Outlines your rights regarding your personal information."
            ],
            DocumentType.TERMS_OF_SERVICE: [
                "Defines your responsibilities and the service limitations.",
                "Explains conditions for account termination.",
                "Outlines the dispute resolution process."
            ]
        }
        return points.get(doc_type, [
            "Contains important legal obligations and rights.",
            "Requires careful review before acceptance."
        ])

class ReportGenerationTool(Tool[ReportGenerationResult]):
    """Agent 6: Report Generation - Creates final legal nutrition label report"""
    
    id: str = "report_generation"
    name: str = "Report Generation"
    description: str = "Generates the final legal nutrition label report"
    args_schema: type[BaseModel] = ReportGenerationArgs
    output_schema: tuple[str, str] = ("ReportGenerationResult", "The final analysis report")

    def run(self, context: ToolRunContext, summary: Summary, obligations: List[Obligation], rights_and_data_usage: List[RightAndDataUsage], 
             red_flags: List[RedFlag], processing_steps: List[ProcessingStep]) -> ReportGenerationResult:
        try:
            total_time = sum(float(step.duration.replace("s", "")) for step in processing_steps)
            
            assembly_line = AIAssemblyLine(
                processing_steps=processing_steps,
                total_processing_time=f"{total_time:.1f}s"
            )

            final_report = AnalysisResult(
                summary=summary,
                obligations=obligations,
                rights_and_data_usage=rights_and_data_usage,
                red_flags=red_flags,
                ai_assembly_line=assembly_line
            )
            
            return ReportGenerationResult(
                final_report=final_report,
                confidence=0.93
            )
        except Exception as e:
            raise ToolHardError(f"Report generation failed: {str(e)}") from e

# Export all tools for registry
PACTGUARD_TOOLS = [
    DocumentIngestionTool(),
    LegalClassificationTool(),
    ClauseExtractionTool(),
    RiskAnalysisTool(),
    PlainEnglishTranslationTool(),
    ReportGenerationTool()
]
import re
import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from portia import Tool, ToolRunContext, ToolHardError

from app.models.schemas import (
    AnalysisResult, DocumentIngestionResult, LegalClassificationResult, ClauseExtractionResult,
    RiskAnalysisResult, PlainEnglishResult, ReportGenerationResult,
    DocumentType, RiskLevel, Sentiment, Summary, ProcessingStep, AIAssemblyLine,
    Obligation, RightAndDataUsage, RedFlag
)

# --- Argument Schemas for Tools ---

class DocumentIngestionArgs(BaseModel):
    document_text: str = Field(description="The raw legal document text to normalize")

class LegalClassificationArgs(BaseModel):
    normalized_text: str = Field(description="The normalized document text to classify")

class ClauseExtractionArgs(BaseModel):
    normalized_text: str = Field(description="The normalized document text")
    document_type: DocumentType = Field(description="The classified document type")
    key_sections: List[str] = Field(description="The identified key sections")

class RiskAnalysisArgs(BaseModel):
    extracted_clauses: List[dict] = Field(description="The extracted legal clauses")

class PlainEnglishTranslationArgs(BaseModel):
    document_type: DocumentType = Field(description="The document type")
    overall_risk: RiskLevel = Field(description="The overall risk level")
    word_count: int = Field(description="The document word count")

class ReportGenerationArgs(BaseModel):
    summary: Summary = Field(description="The plain English summary")
    obligations: List[Obligation] = Field(description="The user obligations")
    rights_and_data_usage: List[RightAndDataUsage] = Field(description="The rights and data usage items")
    red_flags: List[RedFlag] = Field(description="The red flags")
    processing_steps: List[ProcessingStep] = Field(description="The AI assembly line processing steps")


# --- Tool Definitions ---

class DocumentIngestionTool(Tool[DocumentIngestionResult]):
    """Agent 1: Document Ingestion - Normalizes and prepares document content"""
    
    id: str = "document_ingestion"
    name: str = "Document Ingestion"
    description: str = "Normalizes and prepares legal document content for analysis"
    args_schema: type[BaseModel] = DocumentIngestionArgs
    output_schema: tuple[str, str] = ("DocumentIngestionResult", "Normalized text and metadata")

    def run(self, context: ToolRunContext, document_text: str) -> DocumentIngestionResult:
        try:
            normalized_text = self._normalize_text(document_text)
            word_count = len(normalized_text.split())
            
            return DocumentIngestionResult(
                normalized_text=normalized_text,
                detected_language="English",
                word_count=word_count,
                confidence=0.95
            )
        except Exception as e:
            raise ToolHardError(f"Document ingestion failed: {str(e)}") from e
    
    def _normalize_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text.strip())
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        return text

class LegalClassificationTool(Tool[LegalClassificationResult]):
    """Agent 2: Legal Classification - Identifies document type and structure"""
    
    id: str = "legal_classification"
    name: str = "Legal Classification"
    description: str = "Classifies the type of legal document and identifies key sections"
    args_schema: type[BaseModel] = LegalClassificationArgs
    output_schema: tuple[str, str] = ("LegalClassificationResult", "Document type and key sections")

    def run(self, context: ToolRunContext, normalized_text: str) -> LegalClassificationResult:
        try:
            document_type = self._classify_document_type(normalized_text)
            key_sections = self._identify_key_sections(normalized_text, document_type)
            
            return LegalClassificationResult(
                document_type=document_type,
                confidence=0.92,
                key_sections=key_sections
            )
        except Exception as e:
            raise ToolHardError(f"Legal classification failed: {str(e)}") from e
    
    def _classify_document_type(self, text: str) -> DocumentType:
        text_lower = text.lower()
        if any(k in text_lower for k in ["terms of service", "terms of use"]):
            return DocumentType.TERMS_OF_SERVICE
        if any(k in text_lower for k in ["privacy policy", "data collection"]):
            return DocumentType.PRIVACY_POLICY
        if any(k in text_lower for k in ["employment agreement", "employment contract"]):
            return DocumentType.EMPLOYMENT_CONTRACT
        if any(k in text_lower for k in ["software license", "mit license"]):
            return DocumentType.SOFTWARE_LICENSE
        return DocumentType.UNKNOWN
    
    def _identify_key_sections(self, text: str, doc_type: DocumentType) -> List[str]:
        if doc_type == DocumentType.PRIVACY_POLICY:
            return ["Data Collection", "Data Usage", "Data Sharing", "User Rights", "Cookies"]
        if doc_type == DocumentType.TERMS_OF_SERVICE:
            return ["User Obligations", "Service Terms", "Liability", "Termination", "Dispute Resolution"]
        return ["General Terms", "Conditions", "Rights", "Obligations"]

class ClauseExtractionTool(Tool[ClauseExtractionResult]):
    """Agent 3: Clause Extraction - Identifies and extracts specific legal clauses"""
    
    id: str = "clause_extraction"
    name: str = "Clause Extraction"
    description: str = "Extracts and identifies specific legal clauses from the document"
    args_schema: type[BaseModel] = ClauseExtractionArgs
    output_schema: tuple[str, str] = ("ClauseExtractionResult", "List of extracted clauses")

    def run(self, context: ToolRunContext, normalized_text: str, document_type: DocumentType, key_sections: List[str]) -> ClauseExtractionResult:
        try:
            extracted_clauses = self._extract_clauses(normalized_text, key_sections)
            return ClauseExtractionResult(
                extracted_clauses=extracted_clauses,
                confidence=0.89
            )
        except Exception as e:
            raise ToolHardError(f"Clause extraction failed: {str(e)}") from e
    
    def _extract_clauses(self, text: str, sections: List[str]) -> List[dict]:
        clauses = []
        sentences = text.split('. ')
        keywords = {
            "risk": ["liable", "responsibility", "terminate", "breach", "penalty"],
            "data_usage": ["collect", "store", "share", "process", "personal data"],
            "obligation": ["must", "shall", "required", "agree to", "consent"]
        }
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            clause_type = "general"
            for type, kws in keywords.items():
                if any(kw in sentence_lower for kw in kws):
                    clause_type = type
                    break
            
            clauses.append({
                "id": str(uuid.uuid4()),
                "text": sentence.strip(),
                "section": self._classify_clause_section(sentence_lower, sections),
                "type": clause_type
            })
        return clauses[:20]

    def _classify_clause_section(self, text: str, sections: List[str]) -> str:
        for section in sections:
            if any(word in text for word in section.lower().split()):
                return section
        return "General Terms"

class RiskAnalysisTool(Tool[RiskAnalysisResult]):
    """Agent 4: Risk Analysis - Analyzes legal risks and assigns severity scores"""
    
    id: str = "risk_analysis" 
    name: str = "Risk Analysis"
    description: str = "Analyzes legal risks and categorizes clauses by severity"
    args_schema: type[BaseModel] = RiskAnalysisArgs
    output_schema: tuple[str, str] = ("RiskAnalysisResult", "Categorized risks and overall assessment")

    def run(self, context: ToolRunContext, extracted_clauses: List[dict]) -> RiskAnalysisResult:
        try:
            obligations, rights, red_flags = [], [], []
            for clause in extracted_clauses:
                if clause["type"] == "obligation":
                    obligations.append(Obligation(**self._create_item(clause, "obligation")))
                elif clause["type"] == "data_usage":
                    rights.append(RightAndDataUsage(**self._create_item(clause, "data_usage")))
                elif clause["type"] == "risk":
                    red_flags.append(RedFlag(**self._create_item(clause, "red_flag")))
            
            overall_risk = self._calculate_overall_risk(red_flags)
            
            return RiskAnalysisResult(
                obligations=obligations,
                rights_and_data_usage=rights,
                red_flags=red_flags,
                overall_risk=overall_risk,
                confidence=0.87
            )
        except Exception as e:
            raise ToolHardError(f"Risk analysis failed: {str(e)}") from e
    
    def _create_item(self, clause: dict, item_type: str) -> dict:
        item = {
            "id": clause["id"],
            "category": clause["section"],
            "clause": clause["text"][:200],
            "explanation": f"This clause defines a key {item_type.replace('_', ' ')}.",
            "severity": RiskLevel.MEDIUM,
        }
        if item_type == "obligation":
            item["impact"] = "User must comply with this."
        elif item_type == "data_usage":
            item["userProtection"] = "Affects user data and privacy."
        elif item_type == "red_flag":
            item.update({
                "severity": RiskLevel.HIGH,
                "recommendation": "Review this clause carefully.",
                "legalImplications": "Potential for significant legal consequences."
            })
        return item
    
    def _calculate_overall_risk(self, red_flags: List) -> RiskLevel:
        if red_flags:
            return RiskLevel.HIGH
        elif len(red_flags) > 0:
             return RiskLevel.MEDIUM
        return RiskLevel.LOW

class PlainEnglishTranslationTool(Tool[PlainEnglishResult]):
    """Agent 5: Plain English Translation - Converts legal jargon to simple language"""
    
    id: str = "plain_english_translation"
    name: str = "Plain English Translation"
    description: str = "Translates legal jargon into plain English summaries"
    args_schema: type[BaseModel] = PlainEnglishTranslationArgs
    output_schema: tuple[str, str] = ("PlainEnglishResult", "A simplified summary of the document")

    def run(self, context: ToolRunContext, document_type: DocumentType, overall_risk: RiskLevel, word_count: int) -> PlainEnglishResult:
        try:
            reading_time = f"{max(1, word_count // 200)} min read"
            
            sentiment = Sentiment.NEUTRAL
            if overall_risk == RiskLevel.HIGH:
                sentiment = Sentiment.NEGATIVE
            elif overall_risk == RiskLevel.LOW:
                sentiment = Sentiment.POSITIVE

            summary = Summary(
                title=f"Legal Document Analysis: {document_type.value}",
                documentType=document_type,
                sentiment=sentiment,
                keyPoints=self._generate_key_points(document_type),
                riskLevel=overall_risk,
                readingTime=reading_time,
                lastUpdated=datetime.now().isoformat()
            )
            return PlainEnglishResult(simplified_summary=summary, confidence=0.91)
        except Exception as e:
            raise ToolHardError(f"Plain english translation failed: {str(e)}") from e
    
    def _generate_key_points(self, doc_type: DocumentType) -> List[str]:
        points = {
            DocumentType.PRIVACY_POLICY: [
                "Explains how your personal data is collected and used.",
                "Describes data sharing practices with third parties.", 
                "Outlines your rights regarding your personal information."
            ],
            DocumentType.TERMS_OF_SERVICE: [
                "Defines your responsibilities and the service limitations.",
                "Explains conditions for account termination.",
                "Outlines the dispute resolution process."
            ]
        }
        return points.get(doc_type, [
            "Contains important legal obligations and rights.",
            "Requires careful review before acceptance."
        ])

class ReportGenerationTool(Tool[ReportGenerationResult]):
    """Agent 6: Report Generation - Creates final legal nutrition label report"""
    
    id: str = "report_generation"
    name: str = "Report Generation"
    description: str = "Generates the final legal nutrition label report"
    args_schema: type[BaseModel] = ReportGenerationArgs
    output_schema: tuple[str, str] = ("ReportGenerationResult", "The final analysis report")

    def run(self, context: ToolRunContext, summary: Summary, obligations: List[Obligation], rights_and_data_usage: List[RightAndDataUsage], 
             red_flags: List[RedFlag], processing_steps: List[ProcessingStep]) -> ReportGenerationResult:
        try:
            total_time = sum(float(step.duration.replace("s", "")) for step in processing_steps)
            
            assembly_line = AIAssemblyLine(
                processing_steps=processing_steps,
                total_processing_time=f"{total_time:.1f}s"
            )

            final_report = AnalysisResult(
                summary=summary,
                obligations=obligations,
                rights_and_data_usage=rights_and_data_usage,
                red_flags=red_flags,
                ai_assembly_line=assembly_line
            )
            
            return ReportGenerationResult(
                final_report=final_report,
                confidence=0.93
            )
        except Exception as e:
            raise ToolHardError(f"Report generation failed: {str(e)}") from e

# Export all tools for registry
PACTGUARD_TOOLS = [
    DocumentIngestionTool(),
    LegalClassificationTool(),
    ClauseExtractionTool(),
    RiskAnalysisTool(),
    PlainEnglishTranslationTool(),
    ReportGenerationTool()
]
import json
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel

from portia import Tool, ToolRunContext

from app.models.schemas import (
    DocumentIngestionResult, LegalClassificationResult, ClauseExtractionResult,
    RiskAnalysisResult, PlainEnglishResult, ReportGenerationResult,
    DocumentType, RiskLevel, Sentiment,
    Obligation, RightAndDataUsage, RedFlag, Summary, ProcessingStep, AIAssemblyLine
)

class DocumentIngestionTool(Tool):
    """Agent 1: Document Ingestion - Normalizes and prepares document content"""
    
    name = "document_ingestion"
    description = "Normalizes and prepares legal document content for analysis"
    parameters = [
        ToolParameter(
            name="document_text",
            type="string",
            description="The raw legal document text to normalize",
            required=True
        )
    ]

    def call(self, document_text: str) -> ToolCallResult:
        try:
            # Normalize the document text
            normalized_text = self._normalize_text(document_text)
            
            # Detect language (simplified)
            detected_language = "English"  # Could use langdetect in production
            
            # Count words
            word_count = len(normalized_text.split())
            
            result = DocumentIngestionResult(
                normalized_text=normalized_text,
                detected_language=detected_language,
                word_count=word_count,
                confidence=0.95
            )
            
            return ToolCallResult(
                success=True,
                value=result.model_dump()
            )
            
        except Exception as e:
            return ToolCallResult(
                success=False,
                error_message=f"Document ingestion failed: {str(e)}"
            )
    
    def _normalize_text(self, text: str) -> str:
        """Normalize the document text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common encoding issues
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text

class LegalClassificationTool(Tool):
    """Agent 2: Legal Classification - Identifies document type and structure"""
    
    name = "legal_classification"
    description = "Classifies the type of legal document and identifies key sections"
    parameters = [
        ToolParameter(
            name="normalized_text",
            type="string",
            description="The normalized document text to classify",
            required=True
        )
    ]

    def call(self, normalized_text: str) -> ToolCallResult:
        try:
            # Classify document type based on keywords
            document_type = self._classify_document_type(normalized_text)
            
            # Extract key sections
            key_sections = self._identify_key_sections(normalized_text, document_type)
            
            result = LegalClassificationResult(
                document_type=document_type,
                confidence=0.92,
                key_sections=key_sections
            )
            
            return ToolCallResult(
                success=True,
                value=result.model_dump()
            )
            
        except Exception as e:
            return ToolCallResult(
                success=False,
                error_message=f"Legal classification failed: {str(e)}"
            )
    
    def _classify_document_type(self, text: str) -> DocumentType:
        """Classify the document type based on content"""
        text_lower = text.lower()
        
        # Check for terms of service indicators
        tos_keywords = ["terms of service", "terms of use", "user agreement", "service agreement"]
        if any(keyword in text_lower for keyword in tos_keywords):
            return DocumentType.TERMS_OF_SERVICE
        
        # Check for privacy policy indicators
        privacy_keywords = ["privacy policy", "data collection", "personal information", "cookie policy"]
        if any(keyword in text_lower for keyword in privacy_keywords):
            return DocumentType.PRIVACY_POLICY
        
        # Check for employment contract indicators
        employment_keywords = ["employment agreement", "employment contract", "job description", "salary", "benefits"]
        if any(keyword in text_lower for keyword in employment_keywords):
            return DocumentType.EMPLOYMENT_CONTRACT
        
        # Check for software license indicators
        license_keywords = ["software license", "mit license", "gpl", "apache license", "copyright"]
        if any(keyword in text_lower for keyword in license_keywords):
            return DocumentType.SOFTWARE_LICENSE
        
        return DocumentType.UNKNOWN
    
    def _identify_key_sections(self, text: str, doc_type: DocumentType) -> List[str]:
        """Identify key sections based on document type"""
        sections = []
        
        if doc_type == DocumentType.PRIVACY_POLICY:
            sections = ["Data Collection", "Data Usage", "Data Sharing", "User Rights", "Cookies"]
        elif doc_type == DocumentType.TERMS_OF_SERVICE:
            sections = ["User Obligations", "Service Terms", "Liability", "Termination", "Dispute Resolution"]
        elif doc_type == DocumentType.EMPLOYMENT_CONTRACT:
            sections = ["Job Duties", "Compensation", "Benefits", "Termination", "Confidentiality"]
        else:
            sections = ["General Terms", "Conditions", "Rights", "Obligations"]
            
        return sections

class ClauseExtractionTool(Tool):
    """Agent 3: Clause Extraction - Identifies and extracts specific legal clauses"""
    
    name = "clause_extraction"
    description = "Extracts and identifies specific legal clauses from the document"
    parameters = [
        ToolParameter(
            name="normalized_text",
            type="string",
            description="The normalized document text",
            required=True
        ),
        ToolParameter(
            name="document_type",
            type="string", 
            description="The classified document type",
            required=True
        ),
        ToolParameter(
            name="key_sections",
            type="array",
            description="The identified key sections",
            required=True
        )
    ]

    def call(self, normalized_text: str, document_type: str, key_sections: List[str]) -> ToolCallResult:
        try:
            # Extract clauses based on document type and sections
            extracted_clauses = self._extract_clauses(normalized_text, document_type, key_sections)
            
            result = ClauseExtractionResult(
                extracted_clauses=extracted_clauses,
                confidence=0.89
            )
            
            return ToolCallResult(
                success=True,
                value=result.model_dump()
            )
            
        except Exception as e:
            return ToolCallResult(
                success=False,
                error_message=f"Clause extraction failed: {str(e)}"
            )
    
    def _extract_clauses(self, text: str, doc_type: str, sections: List[str]) -> List[dict]:
        """Extract clauses from the document"""
        clauses = []
        sentences = text.split('. ')
        
        # Simple clause extraction based on keywords
        risk_keywords = ["liable", "responsibility", "terminate", "breach", "penalty", "damages"]
        data_keywords = ["collect", "store", "share", "process", "personal data", "information"]
        obligation_keywords = ["must", "shall", "required", "agree to", "consent", "responsible"]
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            clause_data = {
                "id": str(uuid.uuid4()),
                "text": sentence.strip(),
                "section": self._classify_clause_section(sentence_lower, sections),
                "type": "general"
            }
            
            if any(keyword in sentence_lower for keyword in risk_keywords):
                clause_data["type"] = "risk"
                clause_data["severity"] = "High"
            elif any(keyword in sentence_lower for keyword in data_keywords):
                clause_data["type"] = "data_usage"
                clause_data["severity"] = "Medium"
            elif any(keyword in sentence_lower for keyword in obligation_keywords):
                clause_data["type"] = "obligation"
                clause_data["severity"] = "Medium"
            
            clauses.append(clause_data)
        
        return clauses[:20]  # Limit for demo
    
    def _classify_clause_section(self, text: str, sections: List[str]) -> str:
        """Classify which section a clause belongs to"""
        for section in sections:
            if any(word in text for word in section.lower().split()):
                return section
        return "General Terms"

class RiskAnalysisTool(Tool):
    """Agent 4: Risk Analysis - Analyzes legal risks and assigns severity scores"""
    
    name = "risk_analysis" 
    description = "Analyzes legal risks and categorizes clauses by severity"
    parameters = [
        ToolParameter(
            name="extracted_clauses",
            type="array",
            description="The extracted legal clauses",
            required=True
        )
    ]

    def call(self, extracted_clauses: List[dict]) -> ToolCallResult:
        try:
            obligations = []
            rights_and_data_usage = []
            red_flags = []
            
            for clause in extracted_clauses:
                if clause["type"] == "obligation":
                    obligations.append(self._create_obligation(clause))
                elif clause["type"] == "data_usage":
                    rights_and_data_usage.append(self._create_right_and_data_usage(clause))
                elif clause["type"] == "risk" and clause.get("severity") == "High":
                    red_flags.append(self._create_red_flag(clause))
            
            # Determine overall risk level
            overall_risk = self._calculate_overall_risk(obligations, rights_and_data_usage, red_flags)
            
            result = RiskAnalysisResult(
                obligations=obligations,
                rights_and_data_usage=rights_and_data_usage,
                red_flags=red_flags,
                overall_risk=overall_risk,
                confidence=0.87
            )
            
            return ToolCallResult(
                success=True,
                value=result.model_dump()
            )
            
        except Exception as e:
            return ToolCallResult(
                success=False,
                error_message=f"Risk analysis failed: {str(e)}"
            )
    
    def _create_obligation(self, clause: dict) -> dict:
        return {
            "id": clause["id"],
            "category": clause["section"],
            "clause": clause["text"][:200] + "..." if len(clause["text"]) > 200 else clause["text"],
            "explanation": "This clause creates a binding obligation for users.",
            "severity": clause.get("severity", "Medium"),
            "impact": "Users must comply or face potential consequences."
        }
    
    def _create_right_and_data_usage(self, clause: dict) -> dict:
        return {
            "id": clause["id"],
            "category": clause["section"],
            "clause": clause["text"][:200] + "..." if len(clause["text"]) > 200 else clause["text"],
            "explanation": "This clause relates to data collection and usage rights.",
            "severity": clause.get("severity", "Medium"),
            "userProtection": "Users should understand data handling practices."
        }
    
    def _create_red_flag(self, clause: dict) -> dict:
        return {
            "id": clause["id"],
            "category": clause["section"],
            "clause": clause["text"][:200] + "..." if len(clause["text"]) > 200 else clause["text"],
            "explanation": "This clause presents significant legal risks.",
            "severity": "High",
            "recommendation": "Carefully review this clause before agreeing.",
            "legalImplications": "This clause may have serious legal consequences."
        }
    
    def _calculate_overall_risk(self, obligations: List, rights: List, red_flags: List) -> RiskLevel:
        if red_flags:
            return RiskLevel.HIGH
        elif len(obligations) > 3 or len(rights) > 5:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

class PlainEnglishTranslationTool(Tool):
    """Agent 5: Plain English Translation - Converts legal jargon to simple language"""
    
    name = "plain_english_translation"
    description = "Translates legal jargon into plain English summaries"
    parameters = [
        ToolParameter(
            name="document_type",
            type="string",
            description="The document type",
            required=True
        ),
        ToolParameter(
            name="overall_risk",
            type="string",
            description="The overall risk level",
            required=True
        ),
        ToolParameter(
            name="word_count",
            type="integer",
            description="The document word count",
            required=True
        )
    ]

    def call(self, document_type: str, overall_risk: str, word_count: int) -> ToolCallResult:
        try:
            # Create simplified summary
            summary = self._create_plain_english_summary(document_type, overall_risk, word_count)
            
            result = PlainEnglishResult(
                simplified_summary=summary,
                confidence=0.91
            )
            
            return ToolCallResult(
                success=True,
                value=result.model_dump()
            )
            
        except Exception as e:
            return ToolCallResult(
                success=False,
                error_message=f"Plain english translation failed: {str(e)}"
            )
    
    def _create_plain_english_summary(self, doc_type: str, risk_level: str, word_count: int) -> dict:
        # Calculate reading time (average 200 words per minute)
        reading_minutes = max(1, word_count // 200)
        reading_time = f"{reading_minutes} minute{'s' if reading_minutes > 1 else ''}"
        
        # Create key points based on document type
        key_points = self._generate_key_points(doc_type)
        
        return {
            "title": f"Legal Document Analysis: {doc_type}",
            "documentType": doc_type,
            "sentiment": self._determine_sentiment(risk_level),
            "keyPoints": key_points,
            "riskLevel": risk_level,
            "readingTime": reading_time,
            "lastUpdated": datetime.now().isoformat()
        }
    
    def _generate_key_points(self, doc_type: str) -> List[str]:
        if doc_type == "Privacy Policy":
            return [
                "Explains how your personal data is collected",
                "Describes data sharing practices with third parties", 
                "Outlines your rights regarding your personal information"
            ]
        elif doc_type == "Terms of Service":
            return [
                "Defines your responsibilities as a user",
                "Explains service limitations and restrictions",
                "Describes termination conditions"
            ]
        else:
            return [
                "Contains important legal obligations",
                "Includes terms that may affect your rights",
                "Requires careful review before acceptance"
            ]
    
    def _determine_sentiment(self, risk_level: str) -> str:
        if risk_level == "High":
            return "Negative"
        elif risk_level == "Medium":
            return "Neutral" 
        else:
            return "Positive"

class ReportGenerationTool(Tool):
    """Agent 6: Report Generation - Creates final legal nutrition label report"""
    
    name = "report_generation"
    description = "Generates the final legal nutrition label report"
    parameters = [
        ToolParameter(
            name="summary",
            type="object",
            description="The plain English summary",
            required=True
        ),
        ToolParameter(
            name="obligations",
            type="array", 
            description="The user obligations",
            required=True
        ),
        ToolParameter(
            name="rights_and_data_usage",
            type="array",
            description="The rights and data usage items",
            required=True
        ),
        ToolParameter(
            name="red_flags",
            type="array",
            description="The red flags",
            required=True
        ),
        ToolParameter(
            name="processing_steps",
            type="array",
            description="The AI assembly line processing steps",
            required=True
        )
    ]

    def call(self, summary: dict, obligations: List[dict], rights_and_data_usage: List[dict], 
             red_flags: List[dict], processing_steps: List[dict]) -> ToolCallResult:
        try:
            # Calculate total processing time
            total_time = sum(float(step["duration"].replace("s", "")) for step in processing_steps)
            
            # Create final report
            final_report = {
                "summary": summary,
                "obligations": obligations,
                "rights_and_data_usage": rights_and_data_usage,
                "red_flags": red_flags,
                "ai_assembly_line": {
                    "processing_steps": processing_steps,
                    "total_processing_time": f"{total_time:.1f}s"
                }
            }
            
            result = ReportGenerationResult(
                final_report=final_report,
                confidence=0.93
            )
            
            return ToolCallResult(
                success=True,
                value=result.model_dump()
            )
            
        except Exception as e:
            return ToolCallResult(
                success=False,
                error_message=f"Report generation failed: {str(e)}"
            )

# Export all tools for registry
PACTGUARD_TOOLS = [
    DocumentIngestionTool(),
    LegalClassificationTool(),
    ClauseExtractionTool(),
    RiskAnalysisTool(),
    PlainEnglishTranslationTool(),
    ReportGenerationTool()
]
