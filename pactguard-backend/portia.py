"""
Mock Portia module for development/demo purposes
This provides the same interface as the real Portia SDK
"""

from typing import Dict, Any
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
    def __init__(self, storage_class: StorageClass, llm_provider: LLMProvider):
        self.storage_class = storage_class
        self.llm_provider = llm_provider
    
    @classmethod
    def from_default(cls, storage_class: StorageClass, llm_provider: LLMProvider):
        return cls(storage_class, llm_provider)


class PortiaToolRegistry:
    def __init__(self, config: Config):
        self.config = config


class CLIExecutionHooks:
    def __init__(self):
        pass


class Portia:
    def __init__(self, config: Config, tools: PortiaToolRegistry, execution_hooks: CLIExecutionHooks):
        self.config = config
        self.tools = tools
        self.execution_hooks = execution_hooks
    
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
