"""
Mock Portia module for development/demo purposes
This provides the same interface as the real Portia SDK
"""

from typing import Dict, Any, Optional
from enum import Enum
import json
import time


class StorageClass(Enum):
    CLOUD = "cloud"
    LOCAL = "local"


class LLMProvider(Enum):
    GOOGLE = "google"
    OPENAI = "openai"


class Config:
    def __init__(self, storage_class: StorageClass = StorageClass.CLOUD, llm_provider: LLMProvider = LLMProvider.GOOGLE):
        self.storage_class = storage_class
        self.llm_provider = llm_provider
    
    @classmethod
    def from_default(cls, storage_class: StorageClass = StorageClass.CLOUD, llm_provider: LLMProvider = LLMProvider.GOOGLE):
        return cls(storage_class, llm_provider)


class PortiaToolRegistry:
    def __init__(self, config: Config):
        self.config = config


class CLIExecutionHooks:
    def __init__(self):
        pass


class MockPlanRun:
    def __init__(self, task: str):
        self.task = task
        self.id = f"run_{int(time.time())}"
        self.status = "completed"
        self.outputs = MockPlanOutput(task)
        self.result = {"message": f"Mock execution of: {task}"}


class MockPlanOutput:
    def __init__(self, task: str):
        # Generate realistic legal analysis output with proper risk scoring
        if "legal risks" in task.lower() or "analyze" in task.lower():
            self.final_output = self._generate_legal_analysis()
        elif "gmail" in task.lower() or "email" in task.lower():
            self.final_output = "Email sent successfully with legal analysis summary"
        elif "drive" in task.lower():
            self.final_output = self._generate_drive_analysis()
        else:
            self.final_output = f"Analysis completed for: {task[:100]}..."
    
    def _generate_legal_analysis(self):
        return """**LEGAL DOCUMENT RISK ANALYSIS**

**OVERALL RISK SCORE: 7/10 (HIGH RISK)**

**EXECUTIVE SUMMARY:**
This legal document contains several high-risk clauses that could significantly impact your rights and obligations. Key concerns include broad liability limitations, unclear termination procedures, and potentially problematic data handling provisions.

**CRITICAL RISK FACTORS:**

1. **LIABILITY WAIVER (Risk Level: 9/10)**
   - The document contains an extremely broad liability waiver
   - Provider disclaims responsibility for virtually all damages
   - Recommendation: Negotiate narrower liability limitations

2. **DATA PRIVACY CONCERNS (Risk Level: 6/10)**
   - Vague language around data collection and usage
   - No clear data retention or deletion policies
   - Recommendation: Request detailed data handling procedures

3. **TERMINATION CLAUSES (Risk Level: 7/10)**
   - Unilateral termination rights heavily favor provider
   - Short notice periods for contract termination
   - Recommendation: Negotiate mutual termination protections

**BUSINESS IMPACT:**
- **Financial Exposure:** High - Unlimited liability exposure
- **Operational Risk:** Medium - Service disruption potential
- **Compliance Risk:** Medium - Data privacy compliance issues

**IMMEDIATE ACTION REQUIRED:**
1. Legal review of liability clauses before signing
2. Negotiate data handling provisions
3. Consider insurance coverage for excluded liabilities"""

    def _generate_drive_analysis(self):
        return """**GOOGLE DRIVE DOCUMENT ANALYSIS**

**RISK ASSESSMENT: 6/10 (MEDIUM-HIGH RISK)**

Document successfully retrieved and analyzed from Google Drive.

**KEY FINDINGS:**
- Contract contains standard commercial terms with some concerning provisions
- Intellectual property clauses need clarification
- Payment terms are generally favorable
- Force majeure provisions are comprehensive

**RECOMMENDATIONS:**
1. Review IP ownership clauses in Section 5
2. Clarify payment dispute resolution process
3. Consider adding data breach notification requirements"""


class Portia:
    def __init__(self, config: Config, tools: Optional[PortiaToolRegistry] = None, execution_hooks: Optional[CLIExecutionHooks] = None):
        self.config = config
        self.tools = tools
        self.execution_hooks = execution_hooks
    
    def run(self, task: str):
        """
        Mock run method that returns a realistic plan run object
        """
        return MockPlanRun(task)
    
    async def analyze_document(self, document_text: str, analysis_type: str = "legal_analysis") -> Dict[str, Any]:
        """
        Mock document analysis that returns realistic legal analysis results
        """
        # Simulate processing time
        await self._simulate_processing()
        
        # Return realistic mock analysis
        return {
            "analysis_id": f"analysis_{int(time.time())}",
            "document_type": "Legal Document",
            "risk_level": "Medium-High",
            "summary": "This document contains several clauses that may pose risks to users, including broad liability waivers and unclear data usage terms.",
            "key_findings": [
                {
                    "category": "Liability",
                    "severity": "High",
                    "finding": "Broad liability waiver clause limits your legal recourse",
                    "location": "Section 8.2",
                    "recommendation": "Consider negotiating narrower liability limitations"
                },
                {
                    "category": "Data Privacy",
                    "severity": "Medium",
                    "finding": "Vague data collection and usage terms",
                    "location": "Section 4.1",
                    "recommendation": "Request specific details on data handling practices"
                },
                {
                    "category": "Termination",
                    "severity": "Medium",
                    "finding": "Unilateral termination rights favor the service provider",
                    "location": "Section 12.1",
                    "recommendation": "Negotiate mutual termination notice periods"
                }
            ],
            "obligations": [
                "Compliance with all applicable laws and regulations",
                "Maintaining confidentiality of proprietary information",
                "Payment of fees within specified timeframes"
            ],
            "rights": [
                "Access to services as specified in the agreement",
                "Technical support during business hours",
                "Data portability upon contract termination"
            ],
            "concerns": [
                "Broad indemnification clauses",
                "Automatic renewal without clear opt-out",
                "Jurisdiction clauses may limit legal options"
            ],
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "powered_by": "Portia AI - Multi-Agent Legal Analysis"
        }
    
    async def _simulate_processing(self):
        """Simulate real AI processing time"""
        import asyncio
        await asyncio.sleep(2)  # Simulate 2 seconds of processing
