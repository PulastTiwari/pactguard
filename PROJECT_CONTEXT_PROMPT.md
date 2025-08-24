# PactGuard Legal AI Assistant - Complete Project Context

## Project Overview

**PactGuard** is a Legal AI Assistant built for **AgentHacks2025** hackathon submission. It's a full-stack application that integrates **Portia AI** with **Google AI (Gemini)** for intelligent legal document analysis, risk assessment, and automated workflows.

## Technical Architecture

### Frontend Stack

- **Framework**: Next.js 15.2.4 with React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS with PostCSS (@tailwindcss/postcss)
- **UI Components**: shadcn/ui component library
- **Key Features**:
  - Dark/light theme toggle
  - File upload and text analysis
  - Google Drive integration
  - Real-time analysis results
  - Email integration workflow

### Backend Stack

- **Framework**: FastAPI with Python 3.13
- **Server**: Uvicorn ASGI server
- **AI Integration**: Portia AI SDK with Google AI as LLM provider
- **Authentication**: Google OAuth 2.0
- **Services**: Google Drive API, Gmail API
- **Environment**: Virtual environment with pip package management

## Project Structure

```
PactGuard/
├── app/                          # Next.js frontend
│   ├── globals.css              # Global styles with Tailwind
│   ├── layout.tsx               # Root layout with theme provider
│   ├── page.tsx                 # Main application page
│   └── api/                     # API route handlers
│       ├── analyze/route.ts     # Document analysis endpoint
│       ├── analyze-drive-file/route.ts
│       ├── analyze-file/route.ts
│       └── send-email/route.ts
├── components/                   # React components
│   ├── google-script.tsx        # Google APIs integration
│   ├── pactguard-analyzer.tsx   # Main analyzer component
│   ├── portia-analysis-report.tsx
│   ├── theme-provider.tsx       # Dark/light theme context
│   ├── theme-toggle.tsx
│   └── ui/                      # shadcn/ui components
├── pactguard-backend/           # Python FastAPI backend
│   ├── main_portia.py          # FastAPI server entry point
│   ├── portia.py               # Mock Portia SDK implementation
│   ├── .env                    # Environment variables
│   ├── requirements.txt        # Python dependencies
│   └── services/
│       └── pactguard_portia_google.py  # Core AI integration
├── lib/utils.ts                # Utility functions
├── types/index.ts              # TypeScript type definitions
└── Configuration files:
    ├── next.config.mjs         # Next.js configuration
    ├── tailwind.config.js      # Tailwind CSS configuration
    ├── postcss.config.mjs      # PostCSS configuration
    ├── tsconfig.json           # TypeScript configuration
    ├── components.json         # shadcn/ui configuration
    └── package.json            # Node.js dependencies
```

## Key Features & Functionality

### 1. Legal Document Analysis

- **Input Methods**: Direct text input, file upload, Google Drive integration
- **AI Processing**: Portia AI + Google Gemini for legal risk assessment
- **Output**: Structured analysis with risk levels, recommendations, compliance issues

### 2. Google Integration

- **Drive API**: Read documents directly from Google Drive
- **Gmail API**: Send analysis reports via email
- **OAuth 2.0**: Secure authentication for Google services

### 3. Real-time Processing

- **FastAPI Backend**: Asynchronous processing with proper error handling
- **Mock Development**: Compatible mock Portia SDK for development/demo
- **Production Ready**: Real Portia AI integration for live deployment

## API Configuration

### Environment Variables

```bash
# Frontend (.env.local)
GOOGLE_API_KEY=your_google_api_key_here

# Backend (.env)
PORTIA_API_KEY=your_portia_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

###  Security Best Practices

**IMPORTANT: Never commit your .env files or API keys directly to GitHub!**

The `.gitignore` file already includes these environment files to prevent them from being tracked:

```gitignore
# Environment variables - NEVER commit API keys to version control
.env
.env.local
.env.production
.env.staging
```

Your application automatically detects and uses the `GOOGLE_API_KEY` and `PORTIA_API_KEY` from the environment variables, allowing Portia AI and Google services to work correctly without exposing sensitive credentials in your codebase.

### API Endpoints

- **POST /analyze**: Direct text analysis
- **POST /analyze-file**: File upload analysis
- **POST /analyze-drive-file**: Google Drive document analysis
- **POST /send-email**: Email analysis reports

## Core Implementation Details

### Portia AI Integration (`pactguard_portia_google.py`)

```python
class PactGuardPortiaGoogle:
    """
    Production-ready Portia AI integration with:
    - Google AI (Gemini) as LLM provider
    - Cloud storage configuration
    - Comprehensive error handling
    - Logging framework
    - Type safety with Optional annotations
    """

    # Key Methods:
    # - run_legal_analysis(): Document risk assessment
    # - run_gmail_integration(): Email automation
    # - analyze_document_from_drive(): Google Drive integration
```

### Frontend Component (`pactguard-analyzer.tsx`)

- React component with TypeScript
- File upload with drag & drop
- Google Drive file picker
- Real-time analysis display
- Email integration workflow

## Development Setup

### Prerequisites

- Node.js (for frontend)
- Python 3.13+ (for backend)
- Google API credentials
- Portia AI API key

### Installation Commands

```bash
# Frontend
npm install
npm run dev  # Runs on http://localhost:3000

# Backend
cd pactguard-backend
pip3 install -r requirements.txt
python3 main_portia.py  # Runs on http://localhost:8000
```

### Key Dependencies

- **Frontend**: next@15.2.4, react@18, tailwindcss, @tailwindcss/postcss
- **Backend**: fastapi, uvicorn, python-dotenv, pydantic

## Technical Challenges Solved

### 1. Portia SDK Integration

- **Challenge**: Portia SDK not publicly available during development
- **Solution**: Created compatible mock implementation with identical API
- **Result**: Seamless transition from development to production

### 2. Import Resolution

- **Challenge**: `portia.cli` module import errors in static analysis
- **Solution**: Robust fallback import system with type annotations
- **Implementation**:
  ```python
  try:
      from portia.cli import CLIExecutionHooks  # type: ignore[import-untyped]
  except ImportError:
      from portia import CLIExecutionHooks  # Mock fallback
  ```

### 3. Type Safety

- **Challenge**: Optional Portia instance causing type errors
- **Solution**: Type assertions with proper error handling
- **Pattern**: `assert self.portia is not None` before API calls

### 4. Tailwind CSS Configuration

- **Challenge**: PostCSS plugin migration error
- **Solution**: Updated to `@tailwindcss/postcss` package
- **Fix**: Modified `postcss.config.mjs` configuration

## Production Deployment

### Server Configuration

- **Frontend**: Next.js optimized build
- **Backend**: FastAPI with Uvicorn in production mode
- **Environment**: All API keys configured via environment variables
- **Logging**: Comprehensive logging framework for monitoring

### Error Handling

- **Decorator Pattern**: `@handle_portia_exceptions` for consistent error handling
- **Graceful Degradation**: Mock fallback ensures functionality during development
- **User Feedback**: Clear error messages and status indicators

## Hackathon Submission Details

### Built For: AgentHacks2025

### Developer: Pulast Singh Tiwari

### Timeline: Completed under time pressure with 30-minute deadline

### Features Delivered:

-  Full-stack legal AI application
-  Portia AI + Google AI integration
-  Google Drive & Gmail workflows
-  Production-ready deployment
-  Comprehensive error handling
-  Modern UI with dark/light themes
-  TypeScript type safety
-  Clean, documented codebase

## Copyright & Attribution

© 2025 PactGuard. Built by Pulast for AgentHacks2025 using Portia AI.

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Run with Docker
./docker-deploy.sh

# Manual Docker commands
docker-compose build
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

### Docker Configuration

- **Frontend**: Multi-stage build with Node.js 20 Alpine
- **Backend**: Python 3.13 slim with health checks
- **Network**: Bridge network for service communication
- **Ports**: Frontend (3000), Backend (8000)
- **Health Checks**: Automated health monitoring
- **Environment**: Secure API key injection via .env file

### Container Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (Next.js)     │◄──►│   (FastAPI)     │
│   Port: 3000    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘
         │                      │
         └──────────────────────┘
              Docker Network
```

## 🤖 LLM Model Optimization Suggestions

### Current Architecture

- **Primary LLM**: Google AI (Gemini) via Portia AI integration
- **Usage**: Legal document analysis, risk assessment, recommendations generation
- **Fallback**: Mock analysis for development/demo environments

### Recommended LLM Enhancements

#### 1. Multi-Model Strategy

```python
# Implement model routing based on task complexity
def get_optimal_model(task_type, document_length):
    if task_type == "summary" and document_length < 1000:
        return "gemini-flash"  # Fast, cost-effective
    elif task_type == "legal_analysis":
        return "gemini-pro"    # High accuracy
    elif task_type == "complex_reasoning":
        return "o1-preview"    # Advanced reasoning
```

#### 2. Prompt Optimization

- **Legal Domain**: Fine-tune prompts for contract analysis specifics
- **Risk Assessment**: Structured output format for consistent scoring
- **Business Impact**: Template-driven impact analysis generation

#### 3. Caching Strategy

```python
# Implement intelligent caching
@lru_cache(maxsize=128)
def analyze_document_cached(doc_hash, analysis_type):
    # Cache expensive LLM calls for similar documents
    pass
```

#### 4. Model Ensemble

- **Primary**: Portia AI + Gemini for legal reasoning
- **Validation**: Claude/GPT-4 for cross-verification on high-risk documents
- **Specialized**: Legal domain models for contract-specific terms

#### 5. Cost Optimization

- **Token Management**: Implement sliding window for large documents
- **Batch Processing**: Group similar analyses for efficiency
- **Smart Preprocessing**: Extract key sections before LLM analysis

### Implementation Suggestions

1. **Model Router**: `/services/model_router.py` for intelligent model selection
2. **Prompt Library**: `/prompts/legal_templates/` for domain-specific prompts
3. **Cache Layer**: Redis/MongoDB for document analysis caching
4. **Monitoring**: Token usage tracking and cost optimization metrics

---

## Instructions for Another LLM

When working with this project:

1. **Docker First**: Use `./docker-deploy.sh` for consistent environment setup
2. **Start both servers**: Frontend (npm run dev) and Backend (python3 main_portia.py)
3. **Check environment variables**: Ensure API keys are properly configured in .env
4. **Import handling**: The Portia integration uses a fallback system - mock for development, real SDK for production
5. **Type errors**: Use type assertions (`assert self.portia is not None`) when working with Optional types
6. **Error patterns**: Follow the decorator pattern for consistent API error handling
7. **UI updates**: Components use shadcn/ui - maintain consistent styling patterns
8. **API integration**: All endpoints return structured JSON with status, error handling, and timestamps
9. **LLM Optimization**: Consider implementing model routing, prompt templates, and caching for production use
10. **Security**: Always use Docker .env files, never commit API keys to git

The project is designed to work seamlessly in both development (with mocks) and production (with real APIs) environments, with full Docker containerization support.
