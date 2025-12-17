"use client";

import { SEOReport } from "@/types/seo";
import { formatDistanceToNow } from "date-fns";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Clock,
  Image,
  Heading1,
  AlertTriangle,
  ChevronRight,
  Trash2,
} from "lucide-react";

interface ReportCardProps {
  report: SEOReport;
  onClick: () => void;
  onDelete?: () => void;
}

export default function ReportCard({
  report,
  onClick,
  onDelete,
}: ReportCardProps) {
  const getScoreBadge = (score: number) => {
    if (score >= 80)
      return {
        text: "Excellent",
        variant: "default" as const,
        color:
          "bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-400",
      };
    if (score >= 60)
      return {
        text: "Good",
        variant: "secondary" as const,
        color:
          "bg-yellow-100 text-yellow-700 dark:bg-yellow-950 dark:text-yellow-400",
      };
    return {
      text: "Needs Work",
      variant: "destructive" as const,
      color: "bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-400",
    };
  };

  const badge = getScoreBadge(report.seo_score);

  return (
    <Card
      onClick={onClick}
      className="group cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 relative overflow-hidden"
    >
      {/* Score Badge - Top Right */}
      <div className="absolute top-4 right-4 z-10">
        <div
          className={`flex flex-col items-center justify-center w-16 h-16 rounded-xl ${badge.color} shadow-lg`}
        >
          <div className="text-2xl font-bold">{report.seo_score}</div>
          <div className="text-[10px]">/100</div>
        </div>
      </div>

      {/* Delete Button (visible on hover) */}
      {onDelete && (
        <div className="absolute top-4 right-24 z-20 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button
            variant="destructive"
            size="icon"
            className="h-8 w-8 rounded-full shadow-md"
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      )}

      <CardHeader className="pb-3">
        <h3 className="text-lg font-semibold truncate pr-20 group-hover:text-primary transition-colors">
          {report.metrics.title || "Untitled Page"}
        </h3>
        <p className="text-sm text-muted-foreground truncate">{report.url}</p>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Metrics Grid */}
        <div className="grid grid-cols-3 gap-3">
          <div className="flex flex-col items-center p-3 rounded-lg bg-muted/50">
            <Clock className="h-4 w-4 text-blue-600 dark:text-blue-400 mb-1" />
            <div className="text-sm font-bold">
              {report.metrics.load_time
                ? `${report.metrics.load_time}s`
                : "N/A"}
            </div>
            <div className="text-[10px] text-muted-foreground">Load</div>
          </div>
          <div className="flex flex-col items-center p-3 rounded-lg bg-muted/50">
            <Heading1 className="h-4 w-4 text-purple-600 dark:text-purple-400 mb-1" />
            <div className="text-sm font-bold">
              {report.metrics.h1_tags.length}
            </div>
            <div className="text-[10px] text-muted-foreground">H1</div>
          </div>
          <div className="flex flex-col items-center p-3 rounded-lg bg-muted/50">
            <Image className="h-4 w-4 text-pink-600 dark:text-pink-400 mb-1" />
            <div className="text-sm font-bold">
              {report.metrics.images.length}
            </div>
            <div className="text-[10px] text-muted-foreground">Images</div>
          </div>
        </div>

        {/* Issues Warning */}
        {report.metrics.missing_alt_tags > 0 && (
          <div className="flex items-center gap-2 p-2 rounded-lg bg-destructive/10 border border-destructive/20">
            <AlertTriangle className="h-4 w-4 text-destructive flex-shrink-0" />
            <span className="text-xs font-medium text-destructive">
              {report.metrics.missing_alt_tags} missing alt tags
            </span>
          </div>
        )}
      </CardContent>

      <CardFooter className="flex items-center justify-between pt-4 border-t">
        <Badge variant={badge.variant} className={badge.color}>
          {badge.text}
        </Badge>
        <div className="flex items-center gap-1 text-xs text-muted-foreground">
          <Clock className="h-3 w-3" />
          {formatDistanceToNow(new Date(report.created_at), {
            addSuffix: true,
          })}
        </div>
      </CardFooter>

      {/* Hover Arrow */}
      <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
        <ChevronRight className="h-5 w-5 text-primary" />
      </div>
    </Card>
  );
}
