import { Shield, Zap, Brain, Github, ExternalLink } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import PactGuardAnalyzer from "@/components/pactguard-analyzer"

export default function HomePage() {
  return (
    <div className="space-y-8 lg:space-y-12">
      {/* Header with Theme Toggle */}
      <header className="relative">
        <div className="absolute top-0 right-0">
          <ThemeToggle />
        </div>

        <div className="text-center space-y-6 pt-8 sm:pt-0">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="p-2 rounded-xl bg-primary/10 border border-primary/20">
              <Shield className="h-8 w-8 text-primary" aria-hidden="true" />
            </div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text">
              PactGuard
            </h1>
          </div>

          <div className="space-y-4">
            <p className="text-lg sm:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Transform complex legal documents into simple, scannable <span className="text-white font-semibold">"nutrition labels"</span> with our AI Assembly Line
            </p>

            <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
              Democratizing legal literacy through intelligent document analysis and plain-language explanations
            </p>
          </div>

          {/* Feature Highlights */}
          <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-sm">
            <div className="flex items-center gap-2 px-3 py-2 rounded-full bg-muted/50 border">
              <Brain className="h-4 w-4 text-primary" aria-hidden="true" />
              <span className="font-medium">Multi-Agent AI</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-full bg-muted/50 border">
              <Zap className="h-4 w-4 text-primary" aria-hidden="true" />
              <span className="font-medium">Instant Analysis</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-full bg-muted/50 border">
              <Shield className="h-4 w-4 text-primary" aria-hidden="true" />
              <span className="font-medium">Legal Clarity</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Analyzer Component */}
      <section aria-label="Document analyzer">
        <PactGuardAnalyzer />
      </section>

      {/* How It Works Section */}
      <section className="space-y-6" aria-labelledby="how-it-works">
        <h2 id="how-it-works" className="text-2xl font-semibold text-center">
          How the AI Assembly Line Works
        </h2>

        <div className="grid gap-4 sm:gap-6 md:grid-cols-3">
          <Card className="text-center p-6 shadow-sm">
            <CardContent className="space-y-3 p-0">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <span className="text-lg font-bold text-primary">1</span>
              </div>
              <h3 className="font-semibold">Document Ingestion</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Advanced parsing agents break down complex legal text into analyzable components
              </p>
            </CardContent>
          </Card>

          <Card className="text-center p-6 shadow-sm">
            <CardContent className="space-y-3 p-0">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <span className="text-lg font-bold text-primary">2</span>
              </div>
              <h3 className="font-semibold">Multi-Agent Analysis</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Specialized AI agents identify obligations, rights, data usage, and red flags
              </p>
            </CardContent>
          </Card>

          <Card className="text-center p-6 shadow-sm">
            <CardContent className="space-y-3 p-0">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <span className="text-lg font-bold text-primary">3</span>
              </div>
              <h3 className="font-semibold">Nutrition Label</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Results are formatted into digestible, scannable summaries with risk indicators
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center space-y-4 pt-8 border-t border-border/50">
        <div className="flex items-center justify-center gap-4">
          <Button variant="outline" size="sm" asChild>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2">
              <Github className="h-4 w-4" aria-hidden="true" />
              View Source
              <ExternalLink className="h-3 w-3" aria-hidden="true" />
            </a>
          </Button>
        </div>

        <p className="text-sm text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          Powered by the AI Assembly Line - A sophisticated multi-agent workflow for production-ready legal document
          analysis. Built for the hackathon to democratize legal literacy.
        </p>

        <p className="text-xs text-muted-foreground">
          © 2025 PactGuard. Built by Pulast for AgentHacks2025 using Portia AI. This tool provides educational analysis and should not replace professional legal advice.
        </p>
      </footer>
    </div>
  )
}
