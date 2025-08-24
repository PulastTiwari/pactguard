#!/usr/bin/env python3
"""
Simple HTTP test for email functionality
Tests the /api/send-email endpoint directly
"""

import requests
import json

def test_email():
    """Test the email API endpoint"""
    
    # API endpoint
    url = "http://127.0.0.1:8001/api/send-email"
    
    # Sample analysis data
    payload = {
        "analysis": {
            "summary": "Test legal document analysis results",
            "riskScore": 7,
            "riskLevel": "HIGH",
            "keyFindings": [
                "Test finding 1: High liability exposure",
                "Test finding 2: Missing indemnification clause",
                "Test finding 3: Unclear termination terms"
            ],
            "recommendations": [
                "Add comprehensive indemnification clause",
                "Clarify termination procedures",
                "Review liability limitations"
            ]
        },
        "email": "pulast9876@gmail.com",
        "documentName": "Test Contract Analysis"
    }
    
    print("🧪 Testing email API...")
    print(f"📧 Sending to: {payload['email']}")
    print(f"🏢 Backend URL: {url}")
    
    try:
        # Make the request
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=120  # 2 minute timeout
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ EMAIL SENT SUCCESSFULLY!")
            print("📧 Check pulast9876@gmail.com for the analysis report")
            print("💰 Check https://app.portialabs.ai/dashboard/billing for API usage")
        else:
            print(f"❌ Email failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_email()
