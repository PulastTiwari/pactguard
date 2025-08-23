# main.py (Updated Version with File Upload Support)

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from typing import List, Literal, Optional
import datetime
import json

# Import the workflow and document parser
from portia_workflow import run_pactguard_workflow
from document_parser import DocumentParser

# --- Pydantic Models for the final report structure ---
class AnalysisSummary(BaseModel):
    documentType: str
    overallRiskLevel: Literal['Low', 'Medium', 'High', 'Critical']
    keyConcerns: List[str]
    recommendation: str

class ReportItem(BaseModel):
    severity: Literal['Low', 'Medium', 'High', 'Critical']
    title: str
    explanation: str
    originalClause: str

class PactGuardAnalysisReport(BaseModel):
    summary: AnalysisSummary
    redFlags: List[ReportItem]
    obligations: List[ReportItem]
    rightsAndDataUsage: List[ReportItem]
    # Optional field for file metadata
    file_info: Optional[dict] = None

class AnalysisRequest(BaseModel):
    text: str

app = FastAPI(
    title="PactGuard AI Service",
    description="AI Assembly Line for Legal Document Analysis",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "PactGuard AI Service is running with Portia"}

# --- Input Models ---
class DocumentAnalysisRequest(BaseModel):
    text: str

# --- API Endpoints ---
@app.post("/analyze")
async def analyze_document_text(request: DocumentAnalysisRequest):
    """Analyze document text using AI workflow"""
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Document text is required")
        
        # Get current timestamp
        iso_timestamp = datetime.datetime.now().isoformat() + "Z"
        
        # Run the AI analysis workflow
        analysis_result = await run_pactguard_workflow(request.text.strip(), iso_timestamp)
        
        # Parse the JSON response from the AI
        try:
            result_json = json.loads(analysis_result)
            return result_json
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {e}")
            print(f"Raw response: {analysis_result[:500]}...")
            raise HTTPException(status_code=500, detail="AI analysis returned invalid format")
            
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-file")
async def analyze_document_file(
    file: UploadFile = File(..., description="Document file to analyze (PDF, DOCX, TXT)")
):
    """Analyze uploaded document file using AI workflow"""
    try:
        # Validate file
        if not DocumentParser.validate_file(file):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file. Supported formats: PDF, DOCX, TXT (max 10MB)"
            )
        
        # Extract text from file
        try:
            document_text = await DocumentParser.extract_text_from_upload(file)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        if not document_text or not document_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the document")
        
        # Get current timestamp
        iso_timestamp = datetime.datetime.now().isoformat() + "Z"
        
        # Run the AI analysis workflow
        analysis_result = await run_pactguard_workflow(document_text.strip(), iso_timestamp)
        
        # Parse the JSON response from the AI
        try:
            result_json = json.loads(analysis_result)
            # Add metadata about the uploaded file
            result_json["file_info"] = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size_bytes": len(document_text),
                "extracted_length": len(document_text)
            }
            return result_json
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {e}")
            print(f"Raw response: {analysis_result[:500]}...")
            raise HTTPException(status_code=500, detail="AI analysis returned invalid format")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"File analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "supported_formats": ["PDF", "DOCX", "TXT"],
        "max_file_size": "10MB"
    }
