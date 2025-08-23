import type { PactGuardAnalysisReport, Severity, ReportItem } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ShieldAlert,
  ShieldCheck,
  ShieldX,
} from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

interface AnalysisReportProps {
  result: PactGuardAnalysisReport;
}

const severityConfig: {
  [key in Severity]: { color: string; textColor: string; icon: React.ElementType };
} = {
  Low: { color: "bg-green-500", textColor: "text-green-500", icon: ShieldCheck },
  Medium: { color: "bg-yellow-500", textColor: "text-yellow-500", icon: ShieldAlert },
  High: { color: "bg-orange-500", textColor: "text-orange-500", icon: ShieldX },
  Critical: { color: "bg-red-600", textColor: "text-red-600", icon: ShieldX },
};

const getSeverityBadge = (severity: Severity) => {
  const config = severityConfig[severity];
  return (
    <Badge
      variant="default"
      className={`text-xs font-semibold text-white ${config.color}`}
    >
      <config.icon className="w-3 h-3 mr-1.5" />
      {severity}
    </Badge>
  );
};

const ReportSection: React.FC<{
  title: string;
  children: React.ReactNode;
}> = ({ title, children }) => (
  <div className="mb-6">
    <h2 className="text-xl font-bold text-foreground mb-4 pb-2 border-b-2 border-primary/20">
      {title}
    </h2>
    {children}
  </div>
);

const ReportItemCard: React.FC<{ item: ReportItem }> = ({ item }) => (
  <Card className="mb-4 shadow-sm hover:shadow-md transition-shadow duration-300">
    <CardHeader className="pb-3">
      <div className="flex items-start justify-between gap-4">
        <CardTitle className="text-base font-semibold leading-snug">
          {item.title}
        </CardTitle>
        {getSeverityBadge(item.severity)}
      </div>
    </CardHeader>
    <CardContent>
      <p className="text-sm text-muted-foreground mb-4">{item.explanation}</p>
      <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="original-clause" className="border-none">
          <AccordionTrigger className="text-xs font-medium text-primary/80 hover:text-primary py-1">
            Show Original Clause
          </AccordionTrigger>
          <AccordionContent className="mt-2 p-3 bg-muted/50 rounded-md border border-muted">
            <blockquote className="text-xs text-muted-foreground italic leading-relaxed">
              "{item.originalClause}"
            </blockquote>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </CardContent>
  </Card>
);

export default function AnalysisReport({ result }: AnalysisReportProps) {
  const { summary, redFlags, obligations, rightsAndDataUsage } = result;

  const OverallRiskIcon = summary.overallRiskLevel ? severityConfig[summary.overallRiskLevel].icon : ShieldAlert;
  const overallRiskTextColor = summary.overallRiskLevel ? severityConfig[summary.overallRiskLevel].textColor : 'text-yellow-500';


  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8 bg-background rounded-lg shadow-lg border border-border">
      {/* 1. Analysis Summary */}
      <div className="mb-8 p-6 rounded-lg bg-muted/50 border border-muted">
        <div className="flex items-center gap-4 mb-4">
          <OverallRiskIcon
            className={`w-8 h-8 ${overallRiskTextColor}`}
          />
          <div>
            <h1 className="text-2xl font-extrabold text-foreground tracking-tight">
              {summary.documentType}
            </h1>
            <p className="text-sm text-muted-foreground">Analysis Report</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h3 className="font-semibold text-foreground">
              Overall Risk Level
            </h3>
            {summary.overallRiskLevel && getSeverityBadge(summary.overallRiskLevel)}
            <p className="text-sm text-muted-foreground mt-2">
              {summary.recommendation}
            </p>
          </div>
          <div className="space-y-3">
            <h3 className="font-semibold text-foreground">Key Concerns</h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              {summary.keyConcerns.map((concern, index) => (
                <li key={index}>{concern}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* 2. Red Flags */}
      {redFlags && redFlags.length > 0 && (
        <ReportSection title="Red Flags">
          <div className="space-y-4">
            {redFlags.map((item, index) => (
              <ReportItemCard key={index} item={item} />
            ))}
          </div>
        </ReportSection>
      )}

      {/* 3. Your Obligations */}
      {obligations && obligations.length > 0 && (
        <ReportSection title="Your Obligations">
          <div className="space-y-4">
            {obligations.map((item, index) => (
              <ReportItemCard key={index} item={item} />
            ))}
          </div>
        </ReportSection>
      )}

      {/* 4. Rights & Data Usage */}
      {rightsAndDataUsage && rightsAndDataUsage.length > 0 && (
        <ReportSection title="Rights & Data Usage">
          <div className="space-y-4">
            {rightsAndDataUsage.map((item, index) => (
              <ReportItemCard key={index} item={item} />
            ))}
          </div>
        </ReportSection>
      )}
    </div>
  );
}
