"use client";

import { SEOReport } from "@/types/seo";
import { formatDistanceToNow } from "date-fns";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { API_ENDPOINTS, fetchWithAuth } from "@/lib/api";

interface ReportDetailProps {
  report: SEOReport;
  onClose: () => void;
}

export default function ReportDetail({ report, onClose }: ReportDetailProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "gradient-success";
    if (score >= 60) return "gradient-warning";
    return "gradient-error";
  };

  const handleDownload = async () => {
    try {
      const response = await fetchWithAuth(
        `${API_ENDPOINTS.REPORTS}/${report.id}/download`
      );
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `report_${report.id}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error("Failed to download report:", error);
    }
  };

  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="p-0 overflow-hidden w-[calc(100%-2rem)] max-w-4xl max-h-[90vh] sm:rounded-2xl">
        <div className="flex flex-col max-h-[90vh]">
          {/* Header */}
          <DialogHeader className="px-6 pt-6 pb-4 border-b bg-background">
            <div className="flex items-center justify-between gap-4">
              <div className="flex-1 min-w-0">
                <DialogTitle className="text-xl sm:text-2xl truncate">
                  {report.metrics.title || "Untitled Page"}
                </DialogTitle>
                <DialogDescription className="truncate">
                  {report.url}
                </DialogDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
                className="flex-shrink-0"
              >
                <Download className="h-4 w-4 mr-2" />
                PDF
              </Button>
            </div>
          </DialogHeader>

          {/* Body */}
          <div className="px-6 py-6 space-y-6 overflow-y-auto">
            {/* Score Section */}
            <div
              className={`${getScoreColor(
                report.seo_score
              )} rounded-2xl p-8 text-center`}
            >
              <div className="text-6xl font-bold mb-2">{report.seo_score}</div>
              <div className="text-xl opacity-90">SEO Score</div>
              <div className="text-sm opacity-75 mt-2">
                Analyzed{" "}
                {formatDistanceToNow(new Date(report.created_at), {
                  addSuffix: true,
                })}
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="card text-center">
                <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                  {report.metrics.load_time
                    ? `${report.metrics.load_time}s`
                    : "N/A"}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Load Time
                </div>
              </div>
              <div className="card text-center">
                <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                  {report.metrics.h1_tags.length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  H1 Tags
                </div>
              </div>
              <div className="card text-center">
                <div className="text-2xl font-bold text-cyan-600 dark:text-cyan-400">
                  {report.metrics.h2_tags.length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  H2 Tags
                </div>
              </div>
              <div className="card text-center">
                <div className="text-2xl font-bold text-pink-600 dark:text-pink-400">
                  {report.metrics.images.length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Images
                </div>
              </div>
            </div>

            {/* Meta Information */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Meta Information</h3>
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Title
                  </label>
                  <p className="mt-1">{report.metrics.title || "Not found"}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Meta Description
                  </label>
                  <p className="mt-1">
                    {report.metrics.meta_description || "Not found"}
                  </p>
                </div>
              </div>
            </div>

            {/* Heading Structure */}
            {(report.metrics.h1_tags.length > 0 ||
              report.metrics.h2_tags.length > 0) && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-4">
                  Heading Structure
                </h3>
                <div className="space-y-4">
                  {report.metrics.h1_tags.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        H1 Tags
                      </label>
                      <ul className="mt-2 space-y-1">
                        {report.metrics.h1_tags.map((tag, idx) => (
                          <li
                            key={idx}
                            className="text-sm pl-4 border-l-2 border-indigo-500"
                          >
                            {tag}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {report.metrics.h2_tags.length > 0 && (
                    <div>
                      <label className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        H2 Tags
                      </label>
                      <ul className="mt-2 space-y-1">
                        {report.metrics.h2_tags.slice(0, 5).map((tag, idx) => (
                          <li
                            key={idx}
                            className="text-sm pl-4 border-l-2 border-purple-500"
                          >
                            {tag}
                          </li>
                        ))}
                        {report.metrics.h2_tags.length > 5 && (
                          <li className="text-sm text-gray-500 dark:text-gray-400 pl-4">
                            +{report.metrics.h2_tags.length - 5} more
                          </li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* AI Insights */}
            {report.ai_insights && (
              <div className="card bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-950 dark:to-purple-950">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                  AI Insights
                </h3>
                <div className="prose dark:prose-invert max-w-none">
                  <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                    {report.ai_insights.summary}
                  </p>
                </div>

                {report.ai_insights.suggestions.length > 0 && (
                  <div className="mt-6">
                    <h4 className="font-semibold mb-3">Recommendations</h4>
                    <ul className="space-y-2">
                      {report.ai_insights.suggestions.map((suggestion, idx) => (
                        <li key={idx} className="flex items-start gap-3">
                          <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-sm font-medium">
                            {idx + 1}
                          </span>
                          <span className="text-gray-700 dark:text-gray-300 flex-1">
                            {suggestion}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Image Analysis */}
            {report.metrics.images.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-4">Image Analysis</h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">
                      Total Images
                    </span>
                    <span className="font-medium">
                      {report.metrics.images.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">
                      Missing Alt Tags
                    </span>
                    <span
                      className={`font-medium ${
                        report.metrics.missing_alt_tags > 0
                          ? "text-red-600 dark:text-red-400"
                          : "text-green-600 dark:text-green-400"
                      }`}
                    >
                      {report.metrics.missing_alt_tags}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Accessibility & Links */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">
                Accessibility & Links
              </h3>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Broken Links
                  </span>
                  <span
                    className={`font-medium ${
                      report.metrics.broken_links > 0
                        ? "text-red-600 dark:text-red-400"
                        : "text-green-600 dark:text-green-400"
                    }`}
                  >
                    {report.metrics.broken_links}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Language Attribute
                  </span>
                  <span className="font-medium">
                    {report.metrics.accessibility.has_lang
                      ? `Present (${report.metrics.accessibility.lang})`
                      : "Missing"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    Missing Labels
                  </span>
                  <span
                    className={`font-medium ${
                      report.metrics.accessibility.missing_labels_count > 0
                        ? "text-red-600 dark:text-red-400"
                        : "text-green-600 dark:text-green-400"
                    }`}
                  >
                    {report.metrics.accessibility.missing_labels_count}
                  </span>
                </div>
              </div>
            </div>

            {/* Lighthouse Scores */}
            {(report.metrics.performance_score !== null ||
              report.metrics.accessibility_score !== null) && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-4">
                  Lighthouse Scores
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div
                      className={`text-2xl font-bold ${
                        (report.metrics.performance_score || 0) >= 90
                          ? "text-green-600"
                          : (report.metrics.performance_score || 0) >= 50
                          ? "text-orange-500"
                          : "text-red-600"
                      }`}
                    >
                      {report.metrics.performance_score !== null
                        ? Math.round(report.metrics.performance_score)
                        : "N/A"}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      Performance
                    </div>
                  </div>
                  <div className="text-center">
                    <div
                      className={`text-2xl font-bold ${
                        (report.metrics.accessibility_score || 0) >= 90
                          ? "text-green-600"
                          : (report.metrics.accessibility_score || 0) >= 50
                          ? "text-orange-500"
                          : "text-red-600"
                      }`}
                    >
                      {report.metrics.accessibility_score !== null
                        ? Math.round(report.metrics.accessibility_score)
                        : "N/A"}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      Accessibility
                    </div>
                  </div>
                  <div className="text-center">
                    <div
                      className={`text-2xl font-bold ${
                        (report.metrics.best_practices_score || 0) >= 90
                          ? "text-green-600"
                          : (report.metrics.best_practices_score || 0) >= 50
                          ? "text-orange-500"
                          : "text-red-600"
                      }`}
                    >
                      {report.metrics.best_practices_score !== null
                        ? Math.round(report.metrics.best_practices_score)
                        : "N/A"}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      Best Practices
                    </div>
                  </div>
                  <div className="text-center">
                    <div
                      className={`text-2xl font-bold ${
                        (report.metrics.lighthouse_seo_score || 0) >= 90
                          ? "text-green-600"
                          : (report.metrics.lighthouse_seo_score || 0) >= 50
                          ? "text-orange-500"
                          : "text-red-600"
                      }`}
                    >
                      {report.metrics.lighthouse_seo_score !== null
                        ? Math.round(report.metrics.lighthouse_seo_score)
                        : "N/A"}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">SEO</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
