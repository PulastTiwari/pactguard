# PactGuard - An Intelligent Legal Analysis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)](https://www.docker.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7.3-3178C6)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB)](https://www.python.org/)

> **AI-powered legal document analysis platform that transforms complex legal text into actionable insights with quantitative risk assessment.**

PactGuard helps individuals, small businesses, and legal professionals quickly assess legal documents for potential risks, providing structured analysis with numerical risk scores and actionable recommendations.

## Features

**Smart Document Analysis** - AI-powered legal document risk assessment with detailed explanations  
**Quantitative Risk Scoring** - Numerical risk evaluation (1-10 scale) with categorized findings  
**Automated Email Reports** - Professional analysis reports delivered via Gmail integration  
**Google Workspace Integration** - Seamless OAuth 2.0 integration with Drive and Gmail  
**Modern Interface** - Responsive UI with dark/light themes and professional design  
**Easy Deployment** - One-command Docker setup for quick installation  
**Secure  **Secure & Private** Private** - Environment-based configuration with secure credential management  
**High Performance** - Async FastAPI backend with optimized response times

## Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/PulastTiwari/pactguard.git
   cd pactguard
   ```

2. **Configure environment**

   ```bash
   cp .env.docker.template .env
   ```

   Edit `.env` and add your API keys:

   - Get Portia AI key: https://app.portialabs.ai/
   - Get Google AI key: https://makersuite.google.com/app/apikey

3. **Deploy with Docker**

   ```bash
   ./docker-deploy.sh
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8001/docs

### Option 2: Manual Development Setup

Requirements: Node.js 18+, Python 3.11+, API keys

**Backend Setup:**

```bash
cd pactguard-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env  # Add your API keys
uvicorn main_portia:app --host 127.0.0.1 --port 8001 --reload
```

**Frontend Setup:**

```bash
npm install
cp .env.local.template .env.local
npm run dev
```

## 📖 Table of Contents

- [Demo & Screenshots](#-demo--screenshots)
- [Project Vision](#-project-vision)
- [Technical Architecture](#-technical-architecture)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

## Demo & Screenshots

### Live Demo

_(Add your deployed demo link here)_

### Key Workflows

1. **Document Analysis**: Upload or paste legal text for instant AI analysis
2. **Risk Assessment**: Get numerical risk scores with detailed explanations
3. **Email Integration**: Receive professional reports directly in your inbox
4. **Google Drive**: Analyze documents directly from your Drive storage

## Project Vision

### The Problem

Legal document review is complex, time-intensive, and prone to human oversight. Traditional processes lack systematic risk quantification, creating potential blind spots in contract analysis.

### Our Solution

PactGuard bridges the gap between traditional legal workflows and modern AI capabilities, functioning as a force multiplier for legal intelligence rather than a replacement for professional expertise.

### Target Users

- **Individuals & SMEs**: Preliminary risk assessment for contracts and legal documents
- **Legal Practitioners**: Accelerated due diligence and systematic issue flagging
- **Legal Education**: Structured analysis frameworks and pedagogical tools

## Technical Architecture

PactGuard implements a decoupled, service-oriented architecture optimized for scalability and maintainability.

### Frontend Stack

- **Next.js 15.2.4**: React-based framework with server-side rendering
- **TypeScript 5.7.3**: Type-safe development with compile-time error checking
- **Tailwind CSS**: Utility-first styling with custom component library
- **shadcn/ui**: Modern component library with accessibility compliance

### Backend Stack

- **FastAPI 0.115.6**: High-performance async web framework with auto-documentation
- **Python 3.13**: Latest runtime with enhanced performance characteristics
- **Portia AI SDK**: Primary AI orchestration with Google Gemini LLM integration
- **Uvicorn**: ASGI server optimized for async Python applications

### AI Integration

The system's intelligence is powered by Portia AI as the central orchestration engine, integrated with Google Gemini for natural language understanding. Key features include:

```python
# Robust SDK loading with fallback support
try:
    from portia_ai import Portia
    from portia_ai.tools import GoogleDriveTools, GmailTools
    REAL_PORTIA_SDK = True
except ImportError:
    from .portia_mock import Portia, GoogleDriveTools, GmailTools
    REAL_PORTIA_SDK = False

async def run_legal_analysis(self, text: str) -> Dict[str, Any]:
    """Execute comprehensive legal document analysis"""
    try:
        plan_run = await self.client.run_agent(
            agent_id="legal-document-analyzer",
            inputs={"document_text": text},
            tools=self.tools
        )
        return self._parse_analysis_results(plan_run)
    except Exception as e:
        logger.error(f"Legal analysis failed: {e}")
        raise AnalysisException(f"Failed to analyze document: {str(e)}")
```

## 📋 API Documentation

### Core Endpoints

**Document Analysis**

```http
POST /analyze
Content-Type: application/json

{
  "text": "Your legal document text here"
}
```

**File Analysis**

```http
POST /analyze-file
Content-Type: multipart/form-data

file: [document.pdf]
```

**Email Integration**

```http
POST /send-email
Content-Type: application/json

{
  "recipient_email": "user@example.com",
  "analysis_text": "Analysis results...",
  "subject": "Legal Document Analysis Report"
}
```

**Google Drive Integration**

```http
POST /analyze-drive-file
Content-Type: application/json

{
  "file_id": "google_drive_file_id"
}
```

For complete API documentation, visit `/docs` endpoint when running the backend.

## 🤝 Contributing

We welcome contributions from the community! PactGuard is designed to be community-driven and collaborative.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow the existing code style (PEP 8 for Python, Prettier for TypeScript)
- Write clear commit messages
- Update documentation as needed
- Test your changes thoroughly

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Roadmap

### Short Term (Q2 2025)

- Enhanced document type support (NDAs, terms of service, etc.)
- Improved risk scoring algorithms
- Document comparison features
- User authentication and personalized dashboards

### Medium Term (Q3-Q4 2025)

- Browser extension for in-situ analysis
- Public API for third-party integrations
- Enterprise features (SSO, audit logs, multi-tenancy)
- Advanced analytics and insights

### Long Term (2026+)

- Multi-model AI orchestration with intelligent routing
- Legal database integrations (Westlaw, LexisNexis)
- Regulatory compliance checking
- Contract generation capabilities

See [ROADMAP.md](ROADMAP.md) for the complete technical roadmap.

## Security ##  Security & Privacy Privacy

- Environment-based configuration for secure credential management
- No storage of sensitive legal documents on servers
- Encrypted data transmission
- Regular security updates and dependency monitoring

See [SECURITY.md](SECURITY.md) for security policies and reporting procedures.

## 🏆 Recognition

**AgentHacks 2025 Project**

- Developer: Pulast Singh Tiwari
- Timeline: 5-day intensive development period
- Focus: Rapid prototyping with production-ready architecture

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Portia AI](https://www.portia.ai/) for AI orchestration platform
- [Google AI](https://ai.google/) for Gemini LLM integration
- [AgentHacks 2025](https://agenthacks.com/) for the development opportunity
- The open source community for inspiration and tools

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/PulastTiwari/pactguard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PulastTiwari/pactguard/discussions)
- **Email**: [Your contact email]
- **Documentation**: [Project Wiki](https://github.com/PulastTiwari/pactguard/wiki)

---

**Star this repository if PactGuard helps you with legal document analysis!**

Built with love by [Pulast Singh Tiwari](https://github.com/PulastTiwari) for the legal tech community.
