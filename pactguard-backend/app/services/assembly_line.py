"""
PactGuard AI Assembly Line Service

This service orchestrates the 6 specialized agents to process legal documents.
For now, it uses mock implementations to demonstrate the workflow.
"""
import time
from datetime import datetime
from typing import List
import uuid
import random

from app.models.schemas import (
    DocumentAnalysisRequest, AnalysisResult, Summary, ProcessingStep, AIAssemblyLine,
    Obligation, RightAndDataUsage, RedFlag, DocumentType, RiskLevel, Sentiment, ProcessingStatus
)

class PactGuardAssemblyLine:
    """
    AI Assembly Line for legal document analysis
    """
    
    def __init__(self):
        self.processing_steps: List[ProcessingStep] = []
    
    async def analyze_document(self, request: DocumentAnalysisRequest) -> AnalysisResult:
        """
        Main method to analyze a legal document through the AI Assembly Line
        """
        start_time = time.time()
        self.processing_steps = []

        # Simulate the 6-step AI Assembly Line
        await self._run_step("Document Ingestion", 0.5)
        await self._run_step("Legal Classification", 1.0)
        await self._run_step("Clause Extraction", 1.5)
        await self._run_step("Risk Analysis", 2.0)
        await self._run_step("Plain English Translation", 1.5)
        await self._run_step("Report Generation", 0.5)

        # Mock data generation
        summary = self._generate_mock_summary(request)
        obligations = self._generate_mock_obligations()
        rights_and_data_usage = self._generate_mock_rights()
        red_flags = self._generate_mock_red_flags()
        
        total_duration = time.time() - start_time
        
        assembly_line_report = AIAssemblyLine(
            processing_steps=self.processing_steps,
            total_processing_time=f"{total_duration:.2f}s"
        )

        return AnalysisResult(
            summary=summary,
            obligations=obligations,
            rights_and_data_usage=rights_and_data_usage,
            red_flags=red_flags,
            ai_assembly_line=assembly_line_report,
        )

    async def _run_step(self, agent_name: str, duration: float):
        """Simulates a single step in the assembly line."""
        # Simulate work
        time.sleep(duration)
        
        self.processing_steps.append(ProcessingStep(
            agent=agent_name,
            status=ProcessingStatus.COMPLETED,
            duration=f"{duration}s",
            confidence=random.uniform(0.85, 0.99)
        ))

    def _generate_mock_summary(self, request: DocumentAnalysisRequest) -> Summary:
        doc_type_str = request.document_type or "UNKNOWN"
        try:
            doc_type = DocumentType(doc_type_str.replace("_", " ").title())
        except ValueError:
            doc_type = DocumentType.UNKNOWN

        return Summary(
            title=f"Analysis of {doc_type.value}",
            documentType=doc_type,
            sentiment=random.choice(list(Sentiment)),
            keyPoints=[
                "The agreement grants the company a broad license to use your content.",
                "Termination can occur without prior notice.",
                "Dispute resolution is limited to binding arbitration.",
            ],
            riskLevel=random.choice(list(RiskLevel)),
            readingTime=f"{random.randint(5, 15)} min",
            lastUpdated=datetime.utcnow().strftime("%B %d, %Y")
        )

    def _generate_mock_obligations(self) -> List[Obligation]:
        return [
            Obligation(
                id=str(uuid.uuid4()),
                category="Liability",
                clause="You must indemnify the company against any claims arising from your use of the service.",
                explanation="If someone sues the company because of something you did, you have to pay for the legal costs.",
                severity=RiskLevel.HIGH,
                impact="Could result in significant financial loss."
            ),
        ]

    def _generate_mock_rights(self) -> List[RightAndDataUsage]:
        return [
            RightAndDataUsage(
                id=str(uuid.uuid4()),
                category="Account Termination",
                clause="The company can terminate your account at any time without notice.",
                explanation="You could lose access to your account and data without any warning.",
                severity=RiskLevel.HIGH,
                userProtection="Look for services that require a reason ('for cause') or a notice period before termination."
            ),
        ]

    def _generate_mock_red_flags(self) -> List[RedFlag]:
        return [
            RedFlag(
                id=str(uuid.uuid4()),
                category="Dispute Resolution",
                clause="All disputes must be resolved through binding arbitration.",
                explanation="You waive your right to sue in a court of law and have a jury trial.",
                severity=RiskLevel.HIGH,
                recommendation="Be aware that you are giving up significant legal rights. This is common but risky.",
                legalImplications="Arbitration decisions are final and hard to appeal."
            ),
        ]

# Singleton instance of the service
assembly_line = PactGuardAssemblyLine()
import time
from datetime import datetime
from typing import List
import uuid

from app.models.schemas import (
    DocumentAnalysisRequest, AnalysisResult, Summary, ProcessingStep, AIAssemblyLine,
    Obligation, RightAndDataUsage, RedFlag, DocumentType, RiskLevel, Sentiment, ProcessingStatus
)

class PactGuardAssemblyLine:
    """
    AI Assembly Line for legal document analysis
    """
    
    def __init__(self):
        self.processing_steps: List[ProcessingStep] = []
    
    async def analyze_document(self, request: DocumentAnalysisRequest) -> AnalysisResult:
        """
        Main method to analyze a legal document through the AI Assembly Line
        """
        start_time = time.time()
        
        # Step 1: Document Ingestion
        ingestion_start = time.time()
        normalized_text, word_count = self._document_ingestion(request.text)
        ingestion_duration = time.time() - ingestion_start
        self._add_processing_step("Document Ingestion", ingestion_duration, 0.95)
        
        # Step 2: Legal Classification  
        classification_start = time.time()
        document_type, key_sections = self._legal_classification(normalized_text)
        classification_duration = time.time() - classification_start
        self._add_processing_step("Legal Classification", classification_duration, 0.92)
        
        # Step 3: Clause Extraction
        extraction_start = time.time()
        extracted_clauses = self._clause_extraction(normalized_text, key_sections)
        extraction_duration = time.time() - extraction_start
        self._add_processing_step("Clause Extraction", extraction_duration, 0.89)
        
        # Step 4: Risk Analysis
        analysis_start = time.time()
        obligations, rights_data_usage, red_flags, overall_risk = self._risk_analysis(extracted_clauses)
        analysis_duration = time.time() - analysis_start
        self._add_processing_step("Risk Analysis", analysis_duration, 0.87)
        
        # Step 5: Plain English Translation
        translation_start = time.time()
        summary = self._plain_english_translation(document_type, overall_risk, word_count)
        translation_duration = time.time() - translation_start
        self._add_processing_step("Plain English Translation", translation_duration, 0.91)
        
        # Step 6: Report Generation
        report_start = time.time()
        total_time = time.time() - start_time
        ai_assembly_line = AIAssemblyLine(
            processing_steps=self.processing_steps,
            total_processing_time=f"{total_time:.1f}s"
        )
        report_duration = time.time() - report_start
        self._add_processing_step("Report Generation", report_duration, 0.93)
        
        # Create final analysis result
        final_result = AnalysisResult(
            summary=summary,
            obligations=obligations,
            rights_and_data_usage=rights_data_usage,
            red_flags=red_flags,
            ai_assembly_line=ai_assembly_line
        )
        
        return final_result
    
    def _document_ingestion(self, text: str) -> tuple[str, int]:
        """Agent 1: Document Ingestion - Normalizes and prepares document content"""
        # Simulate text normalization
        normalized_text = text.strip()
        normalized_text = " ".join(normalized_text.split())  # Remove extra whitespace
        word_count = len(normalized_text.split())
        
        return normalized_text, word_count
    
    def _legal_classification(self, text: str) -> tuple[DocumentType, List[str]]:
        """Agent 2: Legal Classification - Identifies document type and structure"""
        text_lower = text.lower()
        
        # Classify document type based on keywords
        if any(keyword in text_lower for keyword in ["terms of service", "terms of use", "user agreement"]):
            doc_type = DocumentType.TERMS_OF_SERVICE
            sections = ["User Obligations", "Service Terms", "Liability", "Termination", "Dispute Resolution"]
        elif any(keyword in text_lower for keyword in ["privacy policy", "data collection", "personal information"]):
            doc_type = DocumentType.PRIVACY_POLICY
            sections = ["Data Collection", "Data Usage", "Data Sharing", "User Rights", "Cookies"]
        elif any(keyword in text_lower for keyword in ["employment agreement", "employment contract"]):
            doc_type = DocumentType.EMPLOYMENT_CONTRACT
            sections = ["Job Duties", "Compensation", "Benefits", "Termination", "Confidentiality"]
        elif any(keyword in text_lower for keyword in ["software license", "mit license", "gpl", "apache"]):
            doc_type = DocumentType.SOFTWARE_LICENSE
            sections = ["License Grant", "Restrictions", "Attribution", "Warranty", "Liability"]
        else:
            doc_type = DocumentType.UNKNOWN
            sections = ["General Terms", "Conditions", "Rights", "Obligations"]
        
        return doc_type, sections
    
    def _clause_extraction(self, text: str, sections: List[str]) -> List[dict]:
        """Agent 3: Clause Extraction - Identifies and extracts specific legal clauses"""
        clauses = []
        sentences = text.split('. ')
        
        # Keywords for different clause types
        risk_keywords = ["liable", "responsibility", "terminate", "breach", "penalty", "damages", "lawsuit"]
        data_keywords = ["collect", "store", "share", "process", "personal data", "information", "cookies"]
        obligation_keywords = ["must", "shall", "required", "agree", "consent", "responsible", "comply"]
        
        for sentence in sentences[:15]:  # Limit to first 15 sentences for demo
            if len(sentence.strip()) < 20:  # Skip very short sentences
                continue
                
            sentence_lower = sentence.lower()
            clause_type = "general"
            
            if any(keyword in sentence_lower for keyword in risk_keywords):
                clause_type = "risk"
            elif any(keyword in sentence_lower for keyword in data_keywords):
                clause_type = "data_usage"
            elif any(keyword in sentence_lower for keyword in obligation_keywords):
                clause_type = "obligation"
            
            clauses.append({
                "id": str(uuid.uuid4()),
                "text": sentence.strip(),
                "section": self._classify_clause_section(sentence_lower, sections),
                "type": clause_type
            })
        
        return clauses
    
    def _classify_clause_section(self, text: str, sections: List[str]) -> str:
        """Helper to classify which section a clause belongs to"""
        for section in sections:
            if any(word.lower() in text for word in section.split()):
                return section
        return "General Terms"
    
    def _risk_analysis(self, clauses: List[dict]) -> tuple[List[Obligation], List[RightAndDataUsage], List[RedFlag], RiskLevel]:
        """Agent 4: Risk Analysis - Analyzes legal risks and assigns severity scores"""
        obligations = []
        rights_data_usage = []
        red_flags = []
        
        for clause in clauses:
            clause_text = clause["text"][:200] + ("..." if len(clause["text"]) > 200 else "")
            
            if clause["type"] == "obligation":
                obligations.append(Obligation(
                    id=clause["id"],
                    category=clause["section"],
                    clause=clause_text,
                    explanation="This clause creates a binding obligation that you must follow.",
                    severity=RiskLevel.MEDIUM,
                    impact="You must comply with this requirement to avoid potential consequences."
                ))
            
            elif clause["type"] == "data_usage":
                rights_data_usage.append(RightAndDataUsage(
                    id=clause["id"],
                    category=clause["section"],
                    clause=clause_text,
                    explanation="This clause relates to how your personal data is handled.",
                    severity=RiskLevel.MEDIUM,
                    userProtection="Understanding this helps protect your privacy rights."
                ))
            
            elif clause["type"] == "risk":
                red_flags.append(RedFlag(
                    id=clause["id"],
                    category=clause["section"],
                    clause=clause_text,
                    explanation="This clause presents significant legal risks and should be carefully reviewed.",
                    severity=RiskLevel.HIGH,
                    recommendation="Consider seeking legal advice before agreeing to this clause.",
                    legalImplications="This clause may limit your rights or expose you to liability."
                ))
        
        # Determine overall risk level
        if red_flags:
            overall_risk = RiskLevel.HIGH
        elif len(obligations) > 3 or len(rights_data_usage) > 3:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.LOW
        
        return obligations, rights_data_usage, red_flags, overall_risk
    
    def _plain_english_translation(self, doc_type: DocumentType, risk_level: RiskLevel, word_count: int) -> Summary:
        """Agent 5: Plain English Translation - Converts legal jargon to simple language"""
        
        # Calculate reading time (average 200 words per minute)
        reading_time = f"{max(1, word_count // 200)} min read"
        
        # Generate key points based on document type
        key_points = self._generate_key_points(doc_type)
        
        # Determine sentiment based on risk level
        if risk_level == RiskLevel.HIGH:
            sentiment = Sentiment.NEGATIVE
        elif risk_level == RiskLevel.LOW:
            sentiment = Sentiment.POSITIVE
        else:
            sentiment = Sentiment.NEUTRAL
        
        return Summary(
            title=f"Legal Document Analysis: {doc_type.value}",
            documentType=doc_type,
            sentiment=sentiment,
            keyPoints=key_points,
            riskLevel=risk_level,
            readingTime=reading_time,
            lastUpdated=datetime.now().isoformat()
        )
    
    def _generate_key_points(self, doc_type: DocumentType) -> List[str]:
        """Generate key points based on document type"""
        key_points_map = {
            DocumentType.PRIVACY_POLICY: [
                "Explains how your personal data is collected and used",
                "Describes data sharing practices with third parties",
                "Outlines your rights regarding your personal information",
                "Details cookie usage and tracking technologies"
            ],
            DocumentType.TERMS_OF_SERVICE: [
                "Defines your responsibilities and obligations as a user",
                "Explains service limitations and restrictions", 
                "Describes conditions for account termination",
                "Outlines dispute resolution procedures"
            ],
            DocumentType.EMPLOYMENT_CONTRACT: [
                "Defines job duties and responsibilities",
                "Outlines compensation and benefits",
                "Describes termination conditions",
                "Includes confidentiality and non-compete clauses"
            ],
            DocumentType.SOFTWARE_LICENSE: [
                "Grants specific usage rights for the software",
                "Lists restrictions on software use and distribution",
                "Defines warranty and support limitations",
                "Outlines attribution requirements"
            ]
        }
        
        return key_points_map.get(doc_type, [
            "Contains important legal obligations and terms",
            "Includes provisions that may affect your rights",
            "Requires careful review before acceptance",
            "May have significant legal implications"
        ])
    
    def _add_processing_step(self, agent_name: str, duration: float, confidence: float):
        """Helper to add processing step information"""
        step = ProcessingStep(
            agent=agent_name,
            status=ProcessingStatus.COMPLETED,
            duration=f"{duration:.2f}s",
            confidence=confidence
        )
        self.processing_steps.append(step)

# Global instance
assembly_line = PactGuardAssemblyLine()
