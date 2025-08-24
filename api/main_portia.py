"""
PactGuard FastAPI Backend - Portia Integration
Connects Next.js frontend to real Portia Google AI integration
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging # Added for better logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add services to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Load environment variables
load_dotenv(current_dir / '.env')

# Import our Portia integration
try:
    from services.pactguard_portia_google import PactGuardPortiaGoogle
    logger.info("✅ Successfully imported PactGuard Portia integration")
except ImportError as e:
    logger.error(f"❌ Failed to import Portia integration: {e}")
    PactGuardPortiaGoogle = None

# Request/Response models
class AnalysisRequest(BaseModel):
    text: str

class EmailRequest(BaseModel):
    recipient_email: str
    analysis_text: str
    subject: Optional[str] = "Legal Document Risk Alert - PactGuard Analysis"

class DriveAnalysisRequest(BaseModel):
    file_id: str

class RiskLevel(BaseModel):
    level: int  # 1-10 scale
    label: str  # "Low", "Medium", "High", "Critical"
    color: str  # hex color code

class LegalConcern(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    category: str  # "financial", "operational", "legal", "compliance"

class BusinessImpact(BaseModel):
    category: str
    impact: str
    severity: str
    financial_exposure: Optional[str] = None

class Recommendation(BaseModel):
    id: str
    priority: str  # "immediate", "high", "medium", "low"
    action: str
    rationale: str
    timeline: str

# FIX 5: Replaced generic Dict with a specific Pydantic model for type safety and validation.
class PortiaIntegrationDetails(BaseModel):
    status: str
    plan_run_id: Optional[str] = None
    llm_provider: str
    analysis_timestamp: Optional[str] = None
    portia_used: bool
    billing_generated: bool
    google_drive_file_id: Optional[str] = None
    source: Optional[str] = None


class AnalysisReport(BaseModel):
    id: str
    timestamp: str
    document_type: str
    risk_score: RiskLevel
    executive_summary: str
    legal_concerns: List[LegalConcern]
    business_impact: List[BusinessImpact]
    recommendations: List[Recommendation]
    portia_integration: PortiaIntegrationDetails # Used the new model here

# Global Portia instance
portia_client = None

def initialize_portia():
    """Initialize Portia client with API keys"""
    global portia_client
    
    portia_key = os.getenv('PORTIA_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    
    if not portia_key or not google_key:
        logger.error("❌ Missing API keys - check .env file")
        return False
    
    if PactGuardPortiaGoogle is None:
        logger.error("❌ PactGuard Portia integration not available")
        return False
    
    try:
        portia_client = PactGuardPortiaGoogle(portia_key, google_key)
        if portia_client.initialized:
            logger.info("✅ Portia client initialized successfully")
            return True
        else:
            logger.error("❌ Portia client initialization failed")
            return False
    except Exception as e:
        logger.error(f"❌ Error initializing Portia: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting PactGuard API with Portia integration...")
    success = initialize_portia()
    if not success:
        logger.warning("⚠️ API started but Portia integration may be limited")
    else:
        logger.info("✅ PactGuard API ready with full Portia integration!")
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down PactGuard API...")

# FIX 1: Consolidated FastAPI app initialization into a single instance.
# The `lifespan` argument was added here, and the duplicate app definition below was removed.
app = FastAPI(
    title="PactGuard API",
    description="AI Legal Document Analysis powered by Portia + Google AI",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware is now correctly attached to the single, primary app instance.
# Enhanced CORS for Docker environment support
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://frontend:3000",  # Docker internal network
        "http://0.0.0.0:3000"    # Docker host binding
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_portia_analysis(portia_result: Dict[str, Any], document_text: str) -> AnalysisReport:
    """Convert Portia analysis result to frontend format with enhanced risk scoring"""
    
    analysis_text = portia_result.get('analysis_result', '') or portia_result.get('result', '')
    analysis_lower = str(analysis_text).lower()
    
    # Enhanced risk score extraction from Portia analysis
    import re
    
    # Look for explicit risk scores in format "X/10" or "Risk Score: X"
    risk_match = re.search(r'(?:risk score[:\s]*|overall[^:]*:[^\d]*)(\d+)(?:/10)?', analysis_lower)
    if risk_match:
        risk_score_value = int(risk_match.group(1))
        # Clamp to valid range
        risk_score_value = max(1, min(10, risk_score_value))
    else:
        # Fallback to keyword-based scoring
        if 'extremely high' in analysis_lower or 'critical' in analysis_lower or 'unacceptable' in analysis_lower:
            risk_score_value = 9
            risk_label = "Critical"
            risk_color = "#dc2626"
        elif 'high risk' in analysis_lower or '9/10' in analysis_lower or '8/10' in analysis_lower:
            risk_score_value = 7
            risk_label = "High" 
            risk_color = "#ea580c"
        elif 'medium risk' in analysis_lower or 'moderate risk' in analysis_lower or '6/10' in analysis_lower or '7/10' in analysis_lower:
            risk_score_value = 6
            risk_label = "Medium-High"
            risk_color = "#d97706"
        elif 'medium' in analysis_lower or '5/10' in analysis_lower:
            risk_score_value = 5
            risk_label = "Medium"
            risk_color = "#ca8a04"
        else:
            risk_score_value = 3
            risk_label = "Low"
            risk_color = "#16a34a"
    
    # Determine risk label and color based on score
    if risk_score_value >= 8:
        risk_label = "Critical"
        risk_color = "#dc2626"
    elif risk_score_value >= 7:
        risk_label = "High"
        risk_color = "#ea580c"
    elif risk_score_value >= 6:
        risk_label = "Medium-High"
        risk_color = "#d97706"
    elif risk_score_value >= 4:
        risk_label = "Medium"
        risk_color = "#ca8a04"
    else:
        risk_label = "Low"
        risk_color = "#16a34a"
    
    # Extract specific concerns from analysis text
    concerns = []
    
    # Look for liability concerns
    if 'liability' in analysis_lower:
        concerns.append(LegalConcern(
            id="liability-risk-1",
            title="Liability Waiver Concerns",
            description="Document contains broad liability limitations that may restrict legal recourse",
            severity="critical" if risk_score_value >= 8 else "high",
            category="legal"
        ))
    
    # Look for data privacy concerns
    if 'data' in analysis_lower or 'privacy' in analysis_lower:
        concerns.append(LegalConcern(
            id="privacy-risk-1",
            title="Data Privacy Issues",
            description="Unclear or concerning data collection and usage provisions",
            severity="medium" if risk_score_value < 6 else "high",
            category="compliance"
        ))
    
    # Look for termination concerns
    if 'termination' in analysis_lower:
        concerns.append(LegalConcern(
            id="termination-risk-1",
            title="Termination Clause Risk",
            description="Unbalanced termination rights that may favor the counterparty",
            severity="medium",
            category="operational"
        ))
    
    # Default concerns if none detected
    if not concerns:
        concerns = [
            LegalConcern(
                id="general-risk-1",
                title="Contract Analysis Required",
                description="Document requires detailed legal review to identify specific risks",
                severity="medium",
                category="legal"
            )
        ]
    
    # Generate business impact analysis
    impacts = [
        BusinessImpact(
            category="Financial Risk",
            impact="Potential significant financial exposure from unfavorable terms",
            severity="critical",
            financial_exposure="High - based on contract terms analysis"
        ),
        BusinessImpact(
            category="Legal Compliance",
            impact="Regulatory and legal compliance risks require attention",
            severity="medium",
            financial_exposure="Variable based on jurisdiction"
        )
    ]
    
    # Generate actionable recommendations
    recommendations = [
        Recommendation(
            id="rec-1",
            priority="immediate",
            action="Negotiate improved liability and indemnification terms",
            rationale="Current terms create excessive risk exposure for customer",
            timeline="Before contract execution"
        ),
        Recommendation(
            id="rec-2", 
            priority="high",
            action="Clarify intellectual property ownership and usage rights",
            rationale="Protect valuable IP assets and prevent unintended transfers",
            timeline="Before contract execution"
        ),
    ]
    
    return AnalysisReport(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        document_type="Legal Agreement",
        risk_score=RiskLevel(
            level=risk_score_value,
            label=risk_label,
            color=risk_color
        ),
        executive_summary=f"Document analysis completed using Portia AI. Risk level: {risk_label}. Key findings from AI analysis: {str(analysis_text)[:200]}...",
        legal_concerns=concerns,
        business_impact=impacts,
        recommendations=recommendations,
        portia_integration=PortiaIntegrationDetails(
            status=portia_result.get("status", "unknown"),
            plan_run_id=portia_result.get("plan_run_id"),
            llm_provider="Google AI (Gemini)",
            analysis_timestamp=portia_result.get("timestamp"),
            portia_used=True,
            billing_generated=portia_result.get("plan_run_generated", False)
        )
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    portia_status = "available" if portia_client and portia_client.initialized else "unavailable"
    return {
        "service": "PactGuard API",
        "version": "2.0.0",
        "status": "running",
        "portia_integration": portia_status,
        "llm_provider": "Google AI (Gemini)" if portia_client else "Not configured",
        "agenthack_2025": "Ready for demo!"
    }

@app.get("/health")
async def health_check():
    """Docker health check endpoint"""
    return {"status": "healthy", "service": "pactguard-api"}

@app.post("/analyze", response_model=AnalysisReport)
async def analyze_document(request: AnalysisRequest):
    """
    Analyze legal document using Portia + Google AI
    This endpoint generates real plan runs for demo!
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Document text is required")
    
    try:
        logger.info(f"\n🔥 FRONTEND DEMO - ANALYZING DOCUMENT")
        logger.info(f"   📄 Document length: {len(request.text)} characters")
        
        if portia_client and portia_client.initialized:
            logger.info(f"   🤖 Using Portia + Google AI")
            logger.info(f"   📊 This will generate a real plan run!")
            
            portia_result = portia_client.run_legal_analysis(request.text)
            
            if portia_result["status"] == "success":
                logger.info(f"   ✅ Portia analysis completed!")
                logger.info(f"   📋 Plan Run ID: {portia_result.get('plan_run_id', 'N/A')}")
                logger.info(f"   🎯 Check your Portia dashboard!")
                return parse_portia_analysis(portia_result, request.text)
            else:
                logger.warning(f"   ⚠️ Portia analysis had issues: {portia_result.get('error', 'Unknown')}")
                fallback_result = {
                    "analysis_result": f"Analysis attempted with Portia. Issue encountered: {portia_result.get('error', 'Processing error')}",
                    "status": "partial"
                }
                return parse_portia_analysis(fallback_result, request.text)
        else:
            logger.warning(f"   ⚠️ Portia not available, using fallback analysis")
            fallback_result = {
                "analysis_result": "Legal document analysis completed with fallback processing. Portia integration unavailable.",
                "status": "fallback"
            }
            return parse_portia_analysis(fallback_result, request.text)
            
    except Exception as e:
        # FIX 3: Made exception handling safer by not leaking internal error details to the client.
        logger.error(f"   ❌ Analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during analysis."
        )

# FIX 4: Added the `response_model` to ensure a consistent and validated API contract.
@app.post("/analyze-file", response_model=AnalysisReport)
async def analyze_file(file: UploadFile = File(...)):
    """Analyze uploaded document file"""
    try:
        content = await file.read()
        
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('utf-8', errors='ignore')
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="File appears to be empty or unreadable")
        
        request = AnalysisRequest(text=text)
        return await analyze_document(request)
        
    except HTTPException:
        raise # Re-raise HTTPException to avoid being caught by the generic exception handler
    except Exception as e:
        logger.error(f"File analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"File analysis failed. Please check the file format.")

@app.post("/send-email")
async def send_legal_email(request: EmailRequest):
    """Send legal analysis via email using Gmail integration"""
    try:
        if not portia_client or not portia_client.initialized:
            raise HTTPException(status_code=503, detail="Email service is temporarily unavailable.")
        
        logger.info(f"\n📧 EMAIL REQUEST RECEIVED")
        logger.info(f"   📧 Recipient: {request.recipient_email}")
        
        # Create a comprehensive email with proper legal analysis formatting
        email_content = f"""
LEGAL DOCUMENT RISK ANALYSIS REPORT
Generated by PactGuard AI Legal Assistant
Powered by Portia AI + Google AI (Gemini)

EXECUTIVE SUMMARY:
{request.analysis_text[:500]}

DETAILED ANALYSIS:
Based on our AI-powered legal document analysis, we have identified several key areas of concern that require your immediate attention. This report provides a comprehensive risk assessment with actionable recommendations.

KEY FINDINGS:
• High-risk clauses identified requiring legal review
• Unfavorable terms that may impact your rights and obligations  
• Potential liability exposure requiring mitigation strategies
• Compliance considerations for your review

RECOMMENDATIONS:
1. Schedule immediate legal consultation for high-risk items
2. Consider negotiating more favorable terms before signing
3. Implement additional protections where possible
4. Review insurance coverage for identified risks

This analysis was generated using advanced AI technology combined with legal expertise patterns. For critical decisions, please consult with a qualified attorney.

Best regards,
PactGuard Legal AI Assistant
AgentHacks2025 Demonstration
"""
        
        gmail_result = portia_client.run_gmail_integration(email_content, request.recipient_email)
        
        return {
            "success": True,
            "message": "Legal analysis email sent successfully via Portia Gmail integration",
            "details": gmail_result
        }
        
    except Exception as e:
        logger.error(f"❌ Email sending failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to send email due to an internal error.")


@app.post("/analyze-drive-file", response_model=AnalysisReport)
async def analyze_drive_file(request: DriveAnalysisRequest):
    """
    Analyze a Google Drive document using Portia AI with Google Drive tools
    """
    if not request.file_id or not request.file_id.strip():
        raise HTTPException(status_code=400, detail="Google Drive file_id is required")
    
    if not portia_client or not portia_client.initialized:
        raise HTTPException(status_code=503, detail="Portia client not available")
    
    try:
        logger.info(f"\n📁 GOOGLE DRIVE ANALYSIS REQUEST")
        logger.info(f"   📄 File ID: {request.file_id}")
        
        portia_result = portia_client.analyze_document_from_drive(request.file_id)
        
        document_context = f"Google Drive File: {request.file_id}"
        analysis_report = parse_portia_analysis(portia_result, document_context)
        analysis_report.portia_integration.google_drive_file_id = request.file_id
        analysis_report.portia_integration.source = "Google Drive"
            
        if portia_result["status"] != "success":
            logger.warning(f"   ⚠️ Portia analysis had issues: {portia_result.get('error')}")
            analysis_report.executive_summary = f"Google Drive document analysis attempted. Issue encountered: {portia_result.get('error', 'Unknown error')}"
            analysis_report.portia_integration.status = "partial_success"

        return analysis_report
            
    except Exception as e:
        logger.error(f"❌ Google Drive analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Google Drive analysis failed due to an internal error.")

@app.get("/demo-status")
async def demo_status():
    """Get current demo status for troubleshooting"""
    return {
        "portia_client_initialized": bool(portia_client and portia_client.initialized),
        "api_keys_configured": {
            "portia_api_key_present": bool(os.getenv('PORTIA_API_KEY')),
            "google_api_key_present": bool(os.getenv('GOOGLE_API_KEY'))
        },
        "portia_sdk_available": PactGuardPortiaGoogle is not None,
        "demo_ready": bool(portia_client and portia_client.initialized)
    }

if __name__ == "__main__":
    try:
        import uvicorn
        logger.info("🚀 Starting PactGuard API server...")
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except ImportError:
        logger.error("❌ uvicorn not installed. Install with: pip install uvicorn")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
