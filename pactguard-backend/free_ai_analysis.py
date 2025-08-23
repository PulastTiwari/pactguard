#!/usr/bin/env python3
"""
Free Hugging Face alternative to OpenAI for PactGuard.
This replaces OpenAI calls with free Hugging Face inference.
"""

from typing import Literal
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

load_dotenv()

async def free_legal_analysis(document_text: str, iso_timestamp: str) -> str:
    """
    Analyzes a legal document using a free Hugging Face model.
    The output is structured to match the PactGuardAnalysisReport format.
    """
    
    try:
        # Import Hugging Face client
        from huggingface_hub import InferenceClient
        
        # Initialize client with free token
        hf_token = os.getenv('HF_TOKEN')
        if not hf_token:
            raise Exception("HF_TOKEN not found in environment")
            
        client = InferenceClient(api_key=hf_token)
        
        # Enhanced legal analysis prompt
        analysis_prompt = f"""You are PactGuard, an expert legal document analyzer. Analyze the following document and return a comprehensive JSON analysis.

**Document to Analyze:**
---
{document_text}
---

**Instructions:**
1. Classify the document type: "Terms of Service", "Privacy Policy", "Employment Contract", or "Unknown"
2. Assign a risk score from 0-100 based on how problematic the clauses are
3. Determine overall severity: "low", "medium", "high", or "critical"
4. Extract key clauses into categories: redFlags, obligations, rights, terms
5. Provide plain English explanations for each clause
6. Give actionable recommendations

**Output Format (JSON only, no other text):**
{{
  "documentType": "...",
  "riskScore": ...,
  "overallSeverity": "...",
  "summary": {{
    "keyPoints": ["...", "...", "..."],
    "mainConcerns": ["...", "...", "..."],
    "recommendations": ["...", "...", "..."]
  }},
  "categories": {{
    "redFlags": [
      {{
        "id": "rf-001",
        "clause": "...",
        "explanation": "...",
        "severity": "high"
      }}
    ],
    "obligations": [
      {{
        "id": "ob-001",
        "clause": "...",
        "explanation": "...",
        "severity": "medium"
      }}
    ],
    "rights": [
      {{
        "id": "r-001",
        "clause": "...",
        "explanation": "...",
        "severity": "low"
      }}
    ],
    "terms": [
      {{
        "id": "t-001",
        "clause": "...",
        "explanation": "...",
        "severity": "medium"
      }}
    ]
  }},
  "processedAt": "{iso_timestamp}"
}}"""

        print("🆓 Using free Hugging Face API (DeepSeek V3)...")
        
        # Make API call to free Hugging Face model
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",  # GPT-4 level performance, free
            messages=[
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        result = completion.choices[0].message.content.strip()
        
        # Extract JSON from response
        if '{' in result and '}' in result:
            start_idx = result.find('{')
            end_idx = result.rfind('}') + 1
            json_result = result[start_idx:end_idx]
            
            # Validate JSON
            json.loads(json_result)  # This will raise an exception if invalid
            
            print("✅ Free AI analysis completed successfully!")
            
            # Re-structure the response to match the PactGuardAnalysisReport format
            try:
                # Assuming 'output' is a list of dictionaries from the model
                model_output = json.loads(json_result)
                
                # Heuristically map the old format to the new PactGuardAnalysisReport
                summary = model_output.get("summary", {})
                categories = model_output.get("categories", {})
                
                report = {
                    "summary": {
                        "documentType": model_output.get("documentType", "Unknown"),
                        "overallRiskLevel": map_severity(model_output.get("overallSeverity", "medium")),
                        "keyConcerns": summary.get("mainConcerns", ["No specific concerns identified."]),
                        "recommendation": " ".join(summary.get("recommendations", ["Review carefully."]))
                    },
                    "redFlags": remap_report_items(categories.get("redFlags", [])),
                    "obligations": remap_report_items(categories.get("obligations", [])),
                    "rightsAndDataUsage": remap_report_items(categories.get("rights", []))
                }
                
                return json.dumps(report, indent=2)
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                print(f"Error re-structuring free AI output: {e}")
                # If re-structuring fails, fall back by raising an exception
                raise ValueError("Failed to process response from free AI model.")
        else:
            raise Exception("No JSON found in response")
            
    except Exception as e:
        print(f"⚠️  Free API call failed ({e}), using fallback...")
        
        # Import smart fallback
        from demo_analysis import generate_demo_analysis
        return generate_demo_analysis(document_text, iso_timestamp)

def map_severity(severity: str) -> Literal['Low', 'Medium', 'High', 'Critical']:
    """Maps lowercase severity to the required capitalized format."""
    s_lower = severity.lower()
    if s_lower == "critical":
        return "Critical"
    if s_lower == "high":
        return "High"
    if s_lower == "low":
        return "Low"
    return "Medium"

def remap_report_items(items: list) -> list:
    """Remaps items from the old format to the new ReportItem format."""
    new_items = []
    for item in items:
        new_items.append({
            "title": item.get("clause", "Untitled Clause"),
            "originalClause": item.get("clause", "Original clause text not available."),
            "explanation": item.get("explanation", "No explanation provided."),
            "severity": map_severity(item.get("severity", "medium"))
        })
    return new_items

# Test function
async def test_free_analysis():
    """Test the free analysis"""
    
    sample_doc = """
    PRIVACY POLICY
    
    We collect your personal data including name, email, location.
    We share this data with third-party marketing partners.
    All disputes resolved through binding arbitration.
    We may terminate your account without notice.
    You indemnify us against all legal claims.
    """
    
    print("🧪 Testing Free Legal Analysis...")
    print("-" * 40)
    
    result = await free_legal_analysis(sample_doc, datetime.now().isoformat())
    
    print("📋 Analysis Result:")
    print(result[:200] + "...")
    
    # Check if it's valid JSON
    try:
        parsed = json.loads(result)
        print(f"\n✅ Valid JSON with {len(parsed)} fields")
        print(f"Document Type: {parsed.get('documentType', 'N/A')}")
        print(f"Risk Score: {parsed.get('riskScore', 'N/A')}")
        print(f"Severity: {parsed.get('overallSeverity', 'N/A')}")
    except:
        print("❌ Invalid JSON returned")

if __name__ == "__main__":
    asyncio.run(test_free_analysis())
