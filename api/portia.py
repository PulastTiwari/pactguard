"""
Mock Portia SDK for CI/CD and development environments
This module provides a compatible interface when the real Portia SDK is not available
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime


class LLMProvider:
    """Mock LLM Provider"""
    GOOGLE_VERTEX = "google_vertex"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class StorageClass:
    """Mock Storage Class"""
    LOCAL = "local"
    S3 = "s3"
    GCS = "gcs"


class Config:
    """Mock Config class"""
    def __init__(self, api_key: Optional[str] = None, llm_provider: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.llm_provider = llm_provider
        self.kwargs = kwargs
        logging.info(f"🔧 Mock Config initialized with provider: {llm_provider}")


class PortiaToolRegistry:
    """Mock Tool Registry"""
    def __init__(self):
        logging.info("🔧 Mock PortiaToolRegistry initialized")
    
    def register_tool(self, tool_name: str, **kwargs):
        logging.info(f"🔧 Mock tool registered: {tool_name}")
        return True


class Portia:
    """Mock Portia SDK class for development and testing"""
    
    def __init__(self, config: Config):
        self.config = config
        self.initialized = True
        logging.info("🔧 Mock Portia SDK initialized - no real API calls will be made")
    
    def analyze_document(self, text: str, **kwargs) -> Dict[str, Any]:
        """Mock document analysis"""
        logging.info("🔧 Mock document analysis performed")
        
        # Return a realistic mock response
        return {
            "status": "success",
            "analysis": {
                "risk_level": "medium",
                "risk_score": 6.5,
                "summary": "Mock analysis: This document contains standard terms with moderate risk factors.",
                "key_findings": [
                    "Mock finding: Payment terms are within normal range",
                    "Mock finding: Liability clauses require attention",
                    "Mock finding: Termination conditions are standard"
                ],
                "recommendations": [
                    "Mock recommendation: Review liability limitations",
                    "Mock recommendation: Clarify payment schedules",
                    "Mock recommendation: Consider adding dispute resolution clause"
                ],
                "clauses": [
                    {
                        "type": "payment",
                        "risk_level": "low",
                        "text": "Mock clause: Payment due within 30 days",
                        "concerns": []
                    },
                    {
                        "type": "liability",
                        "risk_level": "medium",
                        "text": "Mock clause: Limited liability provisions",
                        "concerns": ["May not provide adequate protection"]
                    }
                ]
            },
            "metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "word_count": len(text.split()),
                "processing_time": "0.5s",
                "model": "mock-model-v1.0",
                "is_mock": True
            }
        }
    
    def get_risk_assessment(self, text: str) -> Dict[str, Any]:
        """Mock risk assessment"""
        logging.info("🔧 Mock risk assessment performed")
        return {
            "overall_risk": "medium",
            "risk_score": 6.5,
            "risk_factors": [
                "Mock risk: Ambiguous payment terms",
                "Mock risk: Limited warranty provisions"
            ]
        }
    
    def extract_clauses(self, text: str) -> List[Dict[str, Any]]:
        """Mock clause extraction"""
        logging.info("🔧 Mock clause extraction performed")
        return [
            {
                "type": "payment",
                "content": "Mock payment clause",
                "location": "Section 3.1"
            },
            {
                "type": "termination",
                "content": "Mock termination clause",
                "location": "Section 8.2"
            }
        ]


# Module-level logging
logging.info("📦 Mock Portia SDK module loaded - suitable for CI/CD and development")
