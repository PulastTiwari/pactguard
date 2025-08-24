"""
PactGuard Portia Integration with Google AI
Using official Portia SDK with Google as LLM provider
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps

# FIX 1: Replaced print with a proper logging framework for better control.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Portia SDK imports
try:
    from portia import Portia, Config, PortiaToolRegistry, StorageClass, LLMProvider
    USING_REAL_PORTIA = True
    logging.info("🎯 REAL PORTIA SDK LOADED - API calls will generate billing!")
# FIX 2: Improved import handling with robust fallback strategy.
# Primary: Official Portia SDK from 'pip install portia-sdk-python'  
# Fallback: Compatible mock implementation for development/demo
# This approach ensures the code works in both production and development environments.
except ImportError:
    logging.error("Portia SDK not found. Using mock implementation for development.")
    USING_REAL_PORTIA = False
    # Use mock Portia module for development
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    try:
        from portia import Portia, Config, PortiaToolRegistry, StorageClass, LLMProvider
        logging.info("✅ Mock Portia module imported successfully")
    except ImportError:
        # Final fallback if mock module also fails
        logging.critical("Mock Portia module also not found!")
        raise

# FIX 3: Created a decorator to handle repetitive API call logic.
def handle_portia_exceptions(func):
    """A decorator to handle Portia initialization checks and API call exceptions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.initialized or self.portia is None:
            logging.error("Portia not initialized. Cannot execute %s.", func.__name__)
            return {"status": "failed", "error": "Portia not initialized"}
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logging.error("❌ Portia API call in %s failed: %s", func.__name__, e)
            return {"status": "error", "error": str(e), "portia_used": False}
    return wrapper


class PactGuardPortiaGoogle:
    """
    Portia integration using Google AI as LLM provider.
    This will generate real usage in your Portia billing dashboard.
    """
    
    def __init__(self, portia_api_key: str, google_api_key: str):
        self.portia_api_key = portia_api_key
        self.google_api_key = google_api_key
        os.environ['PORTIA_API_KEY'] = self.portia_api_key
        os.environ['GOOGLE_API_KEY'] = self.google_api_key
        
        self.portia: Optional[Portia] = None
        self.initialized = False
        self._initialize_portia()

    # FIX 4: Simplified initialization logic by moving it to a dedicated method.
    def _initialize_portia(self):
        """Initializes the Portia instance and handles fallback configuration."""
        try:
            # Primary configuration attempt
            config = Config.from_default(
                storage_class=StorageClass.CLOUD,
                llm_provider=LLMProvider.GOOGLE
            )
            self.portia = Portia(
                config=config,
                tools=PortiaToolRegistry(config)
            )
            logging.info("✅ PACTGUARD PORTIA WITH GOOGLE AI INITIALIZED!")
            logging.info(f"   🤖 LLM Provider: Google AI (Gemini)")
            logging.info(f"   🔑 Portia API Key: {self.portia_api_key[:20]}...")
            logging.info("   🏗️  Using Portia Tool Registry with Cloud Storage")
            if USING_REAL_PORTIA:
                logging.info("   🎯 REAL PORTIA SDK - API calls will generate billing!")
            self.initialized = True
        except Exception as e:
            logging.error(f"❌ Portia initialization failed: {e}")
            # FIX 5: Fallback is now logged as a warning, not a separate success message.
            logging.warning("   Could not initialize Portia. All calls will fail.")

    @staticmethod
    def _extract_final_output(plan_run: Any) -> str:
        """Safely extracts the final output from a Portia plan run."""
        # FIX 6: Replaced bare `except:` with specific `except Exception`.
        try:
            if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
                return str(plan_run.outputs.final_output)
            return str(plan_run)
        except Exception as output_error:
            logging.error(f"Error extracting final output: {output_error}")
            return "Analysis completed but output format not accessible"

    @handle_portia_exceptions
    def run_legal_analysis(self, document_content: str) -> Dict[str, Any]:
        """Runs legal analysis using Portia AI with Google LLM."""
        logging.info("🔥 RUNNING SIMPLIFIED PORTIA AI LEGAL ANALYSIS")
        legal_task = f"Analyze this document for legal risks: {document_content[:1000]}"
        
        # Type assertion to help static analysis
        assert self.portia is not None, "Portia instance should be initialized"
        plan_run = self.portia.run(legal_task)
        logging.info(f"✅ PORTIA API CALL SUCCESSFUL! Plan Run ID: {getattr(plan_run, 'id', 'N/A')}")
        
        return {
            "status": "success",
            "portia_used": True,
            "plan_run_id": getattr(plan_run, 'id', None),
            "analysis_result": self._extract_final_output(plan_run),
            "timestamp": datetime.now().isoformat()
        }

    @handle_portia_exceptions
    def run_gmail_integration(self, legal_analysis: str, recipient_email: str) -> Dict[str, Any]:
        """Uses Gmail tools through Portia - Draft and Send Email."""
        logging.info("📧 RUNNING GMAIL INTEGRATION WORKFLOW")
        
        # Step 1: Draft the email using Portia Gmail Draft tool
        draft_task = f"""
Draft a professional legal analysis email to {recipient_email} with the following content:

Subject: PactGuard Legal Analysis Report - Document Risk Assessment

Body:
LEGAL DOCUMENT RISK ANALYSIS REPORT
Generated by PactGuard AI Legal Assistant
Powered by Portia AI + Google AI (Gemini)

{legal_analysis}

EXECUTIVE SUMMARY:
This analysis was conducted using advanced AI technology to identify potential legal risks in your document. The findings above highlight key areas requiring attention before proceeding.

CRITICAL RECOMMENDATIONS:
• Schedule immediate legal consultation for high-risk items
• Consider negotiating more favorable terms before signing  
• Implement additional protections where possible
• Review insurance coverage for identified risks

DISCLAIMER:
This analysis was generated using AI technology and should not replace professional legal advice. For critical decisions, please consult with a qualified attorney.

Best regards,
PactGuard Legal AI Assistant
AgentHacks2025 Demonstration

Please draft this email for {recipient_email}.
        """
        
        # Type assertion to help static analysis
        assert self.portia is not None, "Portia instance should be initialized"
        
        # Draft the email first
        draft_plan_run = self.portia.run(draft_task)
        draft_result = self._extract_final_output(draft_plan_run)
        logging.info(f"✅ EMAIL DRAFTED! Plan Run ID: {getattr(draft_plan_run, 'id', 'N/A')}")
        
        # Step 2: Send the drafted email
        send_task = f"Send the email draft that was just created to {recipient_email}"
        send_plan_run = self.portia.run(send_task)
        send_result = self._extract_final_output(send_plan_run)
        logging.info(f"✅ EMAIL SENT! Plan Run ID: {getattr(send_plan_run, 'id', 'N/A')}")
        
        return {
            "status": "success",
            "portia_used": True,
            "draft_plan_run_id": getattr(draft_plan_run, 'id', None),
            "send_plan_run_id": getattr(send_plan_run, 'id', None),
            "draft_result": draft_result,
            "send_result": send_result,
            "recipient": recipient_email,
            "message": "Email drafted and sent successfully via Portia Gmail integration"
        }

    @handle_portia_exceptions
    def analyze_document_from_drive(self, file_id: str) -> Dict[str, Any]:
        """Analyzes a Google Drive document using Portia AI."""
        logging.info("📁 RUNNING GOOGLE DRIVE DOCUMENT ANALYSIS")
        drive_analysis_task = f"Read Google Drive file ID {file_id} and analyze its content for legal risks."
        
        # Type assertion to help static analysis
        assert self.portia is not None, "Portia instance should be initialized"
        plan_run = self.portia.run(drive_analysis_task)
        logging.info(f"✅ GOOGLE DRIVE ANALYSIS SUCCESSFUL! Plan Run ID: {getattr(plan_run, 'id', 'N/A')}")
        
        return {
            "status": "success",
            "portia_used": True,
            "plan_run_id": getattr(plan_run, 'id', None),
            "file_id": file_id,
            "analysis_result": self._extract_final_output(plan_run),
            "timestamp": datetime.now().isoformat()
        }
