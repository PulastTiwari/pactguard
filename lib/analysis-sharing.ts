import type { AnalysisResult } from "../types"

// eslint-disable-next-line @typescript-eslint/no-unused-vars
interface AnalysisShareEvent {
  type: 'analysis-share'
  data: AnalysisResult
}

export class AnalysisSharing {
  private static instance: AnalysisSharing
  private listeners: Set<(data: AnalysisResult) => void> = new Set()
  private latestAnalysis: AnalysisResult | null = null
  
  static getInstance(): AnalysisSharing {
    if (!AnalysisSharing.instance) {
      AnalysisSharing.instance = new AnalysisSharing()
    }
    return AnalysisSharing.instance
  }
  
  shareAnalysis(analysisResult: AnalysisResult): void {
    this.latestAnalysis = analysisResult
    this.listeners.forEach(listener => listener(analysisResult))
    
    // Store in sessionStorage for persistence (client-side only)
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.setItem('pactguard_latest_analysis', JSON.stringify(analysisResult))
      } catch (e) {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const _e = e; // Suppress unused variable warning
        console.warn('Failed to store analysis in sessionStorage:', _e)
      }
    }
    
    // Dispatch custom event for other components (client-side only)
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('pactguard-analysis-shared', { 
        detail: analysisResult 
      }))
    }
  }
  
  onAnalysisShared(listener: (data: AnalysisResult) => void): () => void {
    this.listeners.add(listener)
    
    // Return cleanup function
    return () => {
      this.listeners.delete(listener)
    }
  }
  
  getLatestAnalysis(): AnalysisResult | null {
    if (this.latestAnalysis) {
      return this.latestAnalysis
    }
    // Only access sessionStorage on the client
    if (typeof window === 'undefined') {
      return null
    }
    
    try {
      const stored = sessionStorage.getItem('pactguard_latest_analysis')
      if (stored) {
        this.latestAnalysis = JSON.parse(stored)
        return this.latestAnalysis
      }
      return null
    } catch (e) {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const _e = e; // Suppress unused variable warning
      return null
    }
  }
  
  clearAnalysis(): void {
    this.latestAnalysis = null
    if (typeof window !== 'undefined') {
      try {
        sessionStorage.removeItem('pactguard_latest_analysis')
      } catch (e) {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const _e = e; // Suppress unused variable warning
        // Ignore
      }
    }
    
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('pactguard-analysis-cleared'))
    }
  }
}
