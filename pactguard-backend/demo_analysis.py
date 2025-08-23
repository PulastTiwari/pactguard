import json
import random
from datetime import datetime

def generate_demo_analysis(document_text: str, iso_timestamp: str) -> str:
    """
    Generate a realistic demo analysis based on the PactGuardAnalysisReport structure.
    This simulates the exact workflow and output structure expected by the frontend.
    """
    # Analyze document to determine type
    doc_lower = document_text.lower()
    if "privacy" in doc_lower:
        doc_type = "Privacy Policy"
        risk_score = random.randint(70, 90)
    elif "terms" in doc_lower or "service" in doc_lower:
        doc_type = "Terms of Service"
        risk_score = random.randint(60, 85)
    elif "employment" in doc_lower or "contract" in doc_lower:
        doc_type = "Employment Contract"
        risk_score = random.randint(40, 70)
    else:
        doc_type = "Unknown"
        risk_score = random.randint(50, 80)

    # Determine severity based on risk score
    if risk_score >= 80:
        severity = "Critical"
    elif risk_score >= 65:
        severity = "High"
    elif risk_score >= 45:
        severity = "Medium"
    else:
        severity = "Low"

    # Generate realistic analysis based on the new PactGuardAnalysisReport structure
    analysis = {
        "summary": {
            "documentType": doc_type,
            "overallRiskLevel": severity,
            "keyConcerns": generate_main_concerns(document_text, doc_type),
            "recommendation": " ".join(generate_recommendations(doc_type, severity.lower()))
        },
        "redFlags": generate_red_flags(document_text),
        "obligations": generate_obligations(),
        "rightsAndDataUsage": generate_rights_and_data_usage()
    }

    return json.dumps(analysis, indent=2)


def generate_main_concerns(text: str, doc_type: str) -> list:
    """Generate main concerns (keyConcerns) based on document analysis"""
    concerns = []
    text_lower = text.lower()

    if "arbitration" in text_lower:
        concerns.append("Mandatory arbitration waives right to jury trial.")
    if "indemnify" in text_lower:
        concerns.append("Broad indemnification increases user financial risk.")
    if "data" in text_lower and "third" in text_lower:
        concerns.append("Extensive data sharing with third parties.")
    if "terminate" in text_lower and ("any time" in text_lower or "without notice" in text_lower):
        concerns.append("Service can be terminated without adequate notice.")

    if not concerns:
        concerns.append(f"Standard {doc_type.lower()} concerns apply.")

    return concerns[:3]


def generate_recommendations(doc_type: str, severity: str) -> list:
    """Generate actionable recommendations"""
    recs = [
        "Read the entire document carefully before accepting.",
        "Consider consulting a legal professional for high-risk clauses.",
        "Keep records of all communications and transactions."
    ]

    if severity in ["high", "critical"]:
        recs.insert(0, "HIGH RISK: Strongly consider alternatives to this service.")

    return recs[:4]


def generate_red_flags(text: str) -> list:
    """Generate red flag items in the new ReportItem format"""
    flags = []
    text_lower = text.lower()

    if "arbitration" in text_lower:
        flags.append({
            "title": "Binding Arbitration Clause",
            "originalClause": "The document states that all disputes must be resolved through binding arbitration.",
            "explanation": "This clause significantly limits your legal options, preventing you from suing in a traditional court or participating in class-action lawsuits.",
            "severity": "High"
        })

    if "indemnify" in text_lower:
        flags.append({
            "title": "Broad Indemnification",
            "originalClause": "The document includes a clause requiring you to indemnify the company.",
            "explanation": "You could be held financially responsible for the company's legal fees if they are sued due to your actions, even if you are not at fault.",
            "severity": "High"
        })

    return flags


def generate_obligations() -> list:
    """Generate user obligations in the new ReportItem format"""
    return [{
        "title": "Compliance with Laws",
        "originalClause": "You agree to comply with all applicable laws and regulations when using the service.",
        "explanation": "You are responsible for ensuring your use of the service does not violate any local, state, or federal laws.",
        "severity": "Medium"
    }]


def generate_rights_and_data_usage() -> list:
    """Generate user rights (for rightsAndDataUsage) in the new ReportItem format"""
    return [{
        "title": "Data Access and Deletion",
        "originalClause": "The privacy policy outlines your right to access and request deletion of your personal data.",
        "explanation": "You have the right to know what information is stored about you and to request its removal, which is a key data privacy right.",
        "severity": "Low"
    }]

# Demo function for testing
def demo_analysis():
    """Run a demo analysis to show what Portia would produce"""
    
    sample_document = """
    PRIVACY POLICY
    
    We collect personal information including your name, email, phone number, 
    and location data. We may share this information with third-party partners 
    for marketing purposes. 
    
    All disputes must be resolved through binding arbitration. You agree to 
    indemnify us against all claims. We may terminate your account at any time 
    without notice.
    """
    
    print("🎭 PactGuard Demo Analysis")
    print("=" * 50)
    print()
    print("📄 Sample Document:")
    print(sample_document.strip())
    print()
    print("🤖 Demo Analysis Result (What Portia Would Produce):")
    print("-" * 50)
    
    result = generate_demo_analysis(sample_document, datetime.now().isoformat())
    print(result)
    
    print("\n💡 This demonstrates the exact output format and analysis depth")
    print("   that Portia would provide with real API calls.")

if __name__ == "__main__":
    demo_analysis()
