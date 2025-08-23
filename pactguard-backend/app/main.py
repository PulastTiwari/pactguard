from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.core.config import settings
from app.models.schemas import DocumentAnalysisRequest, AnalysisResult
from app.services.assembly_line import assembly_line

# Load environment variables from .env file
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="PactGuard AI Service",
    description="AI Assembly Line for Legal Document Analysis",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Health check endpoint to ensure the service is running.
    """
    return {"status": "PactGuard AI Service is running"}

# main.py (Updated Version)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from typing import List, Literal
import datetime
import json

# Import the workflow we just created
from portia_workflow import run_pactguard_workflow

# --- Pydantic Models for validation ---
class ClauseAnalysis(BaseModel):
    id: str
    clause: str
    explanation: str
    severity: Literal['low', 'medium', 'high', 'critical']

class Summary(BaseModel):
    keyPoints: List[str]
    mainConcerns: List[str]  
    recommendations: List[str]

class Categories(BaseModel):
    redFlags: List[ClauseAnalysis]
    obligations: List[ClauseAnalysis]
    rights: List[ClauseAnalysis]
    terms: List[ClauseAnalysis]

class AnalysisResult(BaseModel):
    documentType: str
    riskScore: int
    overallSeverity: Literal['low', 'medium', 'high', 'critical']
    summary: Summary
    categories: Categories
    processedAt: str

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

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_document(request: AnalysisRequest):
    """
    This endpoint now runs the live Portia workflow.
    """
    print("Received analysis request. Running Portia workflow...")
    
    try:
        # Prepare the timestamp
        iso_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Execute the workflow
        result_json_str = await run_pactguard_workflow(request.text, iso_timestamp)
        
        print(f"Raw Portia output: {result_json_str}")
        
        # The LLM output is a JSON string, so we parse it
        result_data = json.loads(result_json_str)
        
        # Validate the LLM's output against our Pydantic model
        # This ensures the data contract with the frontend is always met.
        validated_report = AnalysisResult(**result_data)
        
        print("Workflow completed successfully. Returning validated report.")
        return validated_report

    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON from workflow output. Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI model output.")
    except ValidationError as e:
        print(f"Error: Workflow output failed validation. Error: {e}")
        raise HTTPException(status_code=500, detail="AI model output did not match required format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during analysis.")@app.post("/analyze", response_model=AnalysisResult)
async def analyze_document(request: DocumentAnalysisRequest):
    """
    Analyzes a legal document using the PactGuard AI Assembly Line.
    """
    try:
        # Use the assembly line service to analyze the document
        result = await assembly_line.analyze_document(request)
        return result
            
    except Exception as e:
        print(f"Error during analysis: {str(e)}")  # For debugging
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during document analysis: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
