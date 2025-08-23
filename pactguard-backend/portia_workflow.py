# portia_workflow.py

import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Note: Portia client initialization moved inside functions to avoid import errors
# when using free-only mode without OpenAI API key

# portia_workflow.py - FREE AI ONLY VERSION

# 2. Define the enhanced master prompt for the entire workflow
PACTGUARD_MASTER_PROMPT = """
You are PactGuard, a sophisticated AI legal analysis system powered by Portia's tool registry.
Your goal is to analyze a legal document and provide a comprehensive report in a specific JSON format.

**Available Tools**: You have access to web search (Tavily), document research capabilities, and other tools to enhance your analysis.

**Analysis Process**: Perform the following steps in order:

1.  **Document Classification & Research**: 
    - Classify the document type: ["Terms of Service", "Privacy Policy", "Employment Contract", "Unknown"]
    - If needed, use web search to understand current legal standards for this document type

2.  **Enhanced Clause Extraction & Analysis**: 
    - Extract key clauses and categorize them into: `redFlags`, `obligations`, `rights`, and `terms`
    - Research any unusual or potentially problematic clauses
    - Provide simple, one-sentence explanations in plain English
    - Assign severity levels: "low", "medium", "high", or "critical"
    - Generate unique IDs for each clause

3.  **Comprehensive Risk Analysis & Report Generation**: 
    - Calculate a `riskScore` from 0 to 100 based on current legal standards
    - Determine `overallSeverity` considering industry best practices
    - Generate actionable `summary` with `keyPoints`, `mainConcerns`, and `recommendations`
    - Include legal context and comparisons where relevant

**Output Requirements**: 
The final output MUST be a single, valid JSON object. Do NOT include any other text, explanations, or formatting outside of the JSON object.

**JSON Structure:**
```json
{
  "documentType": "...",
  "riskScore": ...,
  "overallSeverity": "...",
  "summary": {
    "keyPoints": ["..."],
    "mainConcerns": ["..."],
    "recommendations": ["..."]
  },
  "categories": {
    "redFlags": [{ "id": "...", "clause": "...", "explanation": "...", "severity": "..." }],
    "obligations": [{ "id": "...", "clause": "...", "explanation": "...", "severity": "..." }],
    "rights": [{ "id": "...", "clause": "...", "explanation": "...", "severity": "..." }],
    "terms": [{ "id": "...", "clause": "...", "explanation": "...", "severity": "..." }]
  },
  "processedAt": "{iso_timestamp}"
}
```

**Legal Document to Analyze:**
---
{document_text}
---

**Instructions**: 
- Use your available tools to enhance the analysis where appropriate
- Focus on providing actionable insights for non-lawyers
- Consider current legal trends and standards in your assessment
- Ensure all JSON fields are properly formatted and complete
"""

async def run_pactguard_workflow(document_text: str, iso_timestamp: str) -> str:
    """
    Runs the entire PactGuard analysis with free alternatives only:
    1. Try free Hugging Face API (requires only HF token) - PRIMARY
    2. Use intelligent demo analysis (always works) - FALLBACK
    
    Note: Portia plan runs require OpenAI API key, so skipping to free alternatives.
    """
    print("🆓 Using FREE AI-only workflow (no OpenAI API key)")
    
    # Skip Portia entirely and go directly to free alternatives
    try:
        print("🚀 Starting free Hugging Face AI analysis...")
        from free_ai_analysis import free_legal_analysis
        result = await free_legal_analysis(document_text, iso_timestamp)
        print("✅ Free AI analysis completed successfully!")
        return result
        
    except Exception as e:
        print(f"❌ Free AI failed: {e}")
        print("🎯 Using intelligent demo analysis (simulates real AI output)...")
        
        # Import and use the smart demo analysis
        from demo_analysis import generate_demo_analysis
        return generate_demo_analysis(document_text, iso_timestamp)

