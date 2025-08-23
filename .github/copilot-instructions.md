<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# PactGuard - AI Legal Document Analyzer

## Project Overview

PactGuard is a hackathon project built for AgentHack 2025 that transforms complex legal documents into simple, scannable "nutrition labels" using a sophisticated AI Assembly Line architecture powered by the Portia SDK.

## Architecture

- **Frontend**: Next.js 14 + TypeScript + Shadcn UI + Tailwind CSS
- **Backend**: Python + Portia SDK (simulated with mock API for demo)
- **AI Assembly Line**: 6 specialized agents working in sequence

## Key Components

### Frontend (`/app`, `/components`)

- **Main App**: `app/page.tsx` - Landing page with project explanation
- **Analyzer**: `components/pactguard-analyzer.tsx` - Main analysis interface
- **Report**: `components/analysis-report.tsx` - Results visualization
- **API**: `app/api/analyze/route.ts` - Mock API simulating Portia workflow

### Backend (`/backend`)

- **Integration**: `pactguard_portia.py` - Shows how Portia SDK would be used
- **Documentation**: Explains the production multi-agent architecture

### Types (`/types`)

- **Interfaces**: Complete TypeScript definitions for all data structures

## Multi-Agent Workflow

1. **Document Ingestion** - Normalizes content
2. **Legal Classification** - Categorizes document type
3. **Clause Extraction** - Identifies specific legal clauses
4. **Risk Analysis** - Assigns risk scores
5. **Plain English Translation** - Converts legal jargon
6. **Report Generation** - Creates nutrition label

## Winning Strategy

- **Technical Sophistication**: Multi-agent vs monolithic approach
- **Production Ready**: Real architecture using Portia SDK
- **User Impact**: Democratizes legal literacy
- **Innovation**: Legal "nutrition labels" + AI Assembly Line visualization

## Development Guidelines

- Use TypeScript for all code
- Follow Next.js 14 App Router patterns
- Maintain responsive design with Tailwind CSS
- Simulate realistic Portia SDK workflows
- Focus on user experience and visual polish
