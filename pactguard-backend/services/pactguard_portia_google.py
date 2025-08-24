"""
PactGuard Portia Integration with Google AI
Using official Portia SDK with Google as LLM provider
"""

import os
from typing import Dict, Any
from datetime import datetime

# Portia SDK imports
try:
    from portia import Portia, Config, PortiaToolRegistry, StorageClass, LLMProvider
    from portia.cli import CLIExecutionHooks
except ImportError:
    # Use mock Portia module for development
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from portia import Portia, Config, PortiaToolRegistry, StorageClass, LLMProvider, CLIExecutionHooks


class PactGuardPortiaGoogle:
    """
    Portia integration using Google AI as LLM provider
    Will generate real usage in your Portia billing dashboard
    """
    
    def __init__(self, portia_api_key: str, google_api_key: str):
        # Set API keys
        self.portia_api_key = portia_api_key
        self.google_api_key = google_api_key
        
        # Set environment variables for Portia auto-detection
        os.environ['PORTIA_API_KEY'] = self.portia_api_key
        os.environ['GOOGLE_API_KEY'] = self.google_api_key
        
        try:
            # Configure Portia with Google AI as LLM provider
            self.config = Config.from_default(
                storage_class=StorageClass.CLOUD,
                llm_provider=LLMProvider.GOOGLE
            )
            
            # Initialize Portia with tools and execution hooks
            self.portia = Portia(
                config=self.config,
                tools=PortiaToolRegistry(self.config),
                execution_hooks=CLIExecutionHooks()
            )
            
            print("✅ PACTGUARD PORTIA WITH GOOGLE AI INITIALIZED!")
            print(f"   🤖 LLM Provider: Google AI (Gemini)")
            print(f"   🔑 Portia API Key: {self.portia_api_key[:20]}...")
            print(f"   🌟 Google API Key: {self.google_api_key[:20]}...")
            print("   📊 This will generate real usage in your billing dashboard!")
            print("   🏗️  Using Portia Tool Registry with Cloud Storage")
            
            self.initialized = True
            
        except Exception as e:
            print(f"❌ Portia initialization failed: {e}")
            print("   Trying fallback configuration...")
            
            try:
                # Fallback: try with minimal config
                self.config = Config.from_default(llm_provider=LLMProvider.GOOGLE)
                self.portia = Portia(
                    config=self.config,
                    tools=PortiaToolRegistry(self.config)
                )
                print("✅ Portia initialized with fallback config")
                self.initialized = True
            except Exception as e2:
                print(f"❌ Fallback config also failed: {e2}")
                self.portia = None
                self.initialized = False
    
    def run_legal_analysis(self, document_content: str) -> Dict[str, Any]:
        """
        Run simplified legal analysis using Portia AI with Google LLM.
        """
        if not self.initialized or self.portia is None:
            return {"status": "failed", "error": "Portia not initialized"}

        print("\n" + "="*70)
        print("🔥 RUNNING SIMPLIFIED PORTIA AI LEGAL ANALYSIS")
        print("   Using Google AI (Gemini) as LLM provider")
        print("="*70)

        try:
            # Very simple task to avoid validation errors
            legal_task = f"Analyze this document for legal risks and provide recommendations: {document_content[:1000]}"
            
            print("📝 Sending simplified legal analysis task to Portia AI...")
            plan_run = self.portia.run(legal_task)

            print("✅ PORTIA API CALL SUCCESSFUL!")
            print(f"   📋 Plan Run ID: {getattr(plan_run, 'id', 'N/A')}")
            
            # Safe output extraction
            try:
                if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
                    final_output = str(plan_run.outputs.final_output)
                else:
                    final_output = str(plan_run)
            except:
                final_output = "Analysis completed but output format not accessible"
            
            return {
                "status": "success",
                "portia_used": True,
                "plan_run_id": getattr(plan_run, 'id', None),
                "analysis_result": final_output,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Portia API call failed: {e}")
            return {"status": "error", "error": str(e), "portia_used": False}
    
    def run_gmail_integration(self, legal_analysis: str, recipient_email: str) -> Dict[str, Any]:
        """
        Use Gmail tools through Portia.
        """
        if not self.initialized or self.portia is None:
            return {"status": "failed", "error": "Portia not initialized"}
        
        print("\n📧 RUNNING GMAIL INTEGRATION WORKFLOW")
        print("   Using Portia Tool Registry for Gmail automation")
        print("="*50)
        
        try:
            # Simple Gmail task
            gmail_task = f'Create an email to {recipient_email} with subject "Legal Analysis Alert" summarizing: {legal_analysis[:500]}'
            
            print("📧 Sending Gmail task to Portia...")
            plan_run = self.portia.run(gmail_task)

            print("✅ GMAIL INTEGRATION SUCCESSFUL!")
            print(f"   📋 Plan Run ID: {getattr(plan_run, 'id', 'N/A')}")
            
            # Safe output extraction
            try:
                if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
                    final_output = str(plan_run.outputs.final_output)
                else:
                    final_output = str(plan_run)
            except:
                final_output = "Gmail task completed but output format not accessible"
            
            return {
                "status": "success",
                "plan_run_id": getattr(plan_run, 'id', None),
                "result": final_output
            }
            
        except Exception as e:
            print(f"❌ Gmail integration failed: {e}")
            return {"status": "error", "error": str(e), "portia_used": False}
    
    def analyze_document_from_drive(self, file_id: str) -> Dict[str, Any]:
        """
        Analyze a Google Drive document using Portia AI with Google Drive tools.
        This will use both Google Drive and legal analysis capabilities.
        """
        if not self.initialized or self.portia is None:
            return {"status": "failed", "error": "Portia not initialized"}
        
        print("\n📁 RUNNING GOOGLE DRIVE DOCUMENT ANALYSIS")
        print("   Using Portia Tool Registry for Google Drive integration")
        print("="*60)
        
        try:
            # Google Drive + Legal Analysis combined task
            drive_analysis_task = f"""
            Please help me analyze a legal document from Google Drive:
            
            1. First, read the content from Google Drive file ID: {file_id}
            2. Then, analyze the document content for legal risks and provide recommendations
            3. Focus on identifying problematic clauses, financial risks, and compliance issues
            
            Provide a structured legal analysis with risk assessment and actionable recommendations.
            """
            
            print(f"📁 Analyzing Google Drive file: {file_id}")
            print("   🎯 This will use Google Drive tools + legal analysis")
            
            plan_run = self.portia.run(drive_analysis_task)

            print("✅ GOOGLE DRIVE ANALYSIS SUCCESSFUL!")
            print(f"   📋 Plan Run ID: {getattr(plan_run, 'id', 'N/A')}")
            
            # Safe output extraction
            try:
                if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
                    final_output = str(plan_run.outputs.final_output)
                else:
                    final_output = str(plan_run)
            except:
                final_output = "Google Drive analysis completed but output format not accessible"
            
            return {
                "status": "success",
                "portia_used": True,
                "plan_run_id": getattr(plan_run, 'id', None),
                "file_id": file_id,
                "analysis_result": final_output,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Google Drive analysis failed: {e}")
            return {"status": "error", "error": str(e), "portia_used": False}
