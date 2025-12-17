"use client";

import { useState, useEffect } from "react";
import URLForm from "@/components/URLForm";
import ReportCard from "@/components/ReportCard";
import ReportDetail from "@/components/ReportDetail";
import { SEOReport } from "@/types/seo";
import { API_ENDPOINTS, fetchWithAuth } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  LayoutGrid,
  List,
  TrendingUp,
  CheckCircle2,
  Trash2,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { ThemeToggle } from "@/components/theme-toggle";
import { LogOut } from "lucide-react";

export default function Home() {
  const [reports, setReports] = useState<SEOReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<SEOReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<"grid" | "table">("grid");
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, [router]);

  const fetchReports = async () => {
    try {
      const response = await fetchWithAuth(
        `${API_ENDPOINTS.REPORTS}?page=1&page_size=20`
      );
      if (response.ok) {
        const data = await response.json();
        setReports(data.reports);
      }
    } catch (error) {
      console.error("Failed to fetch reports:", error);
    } finally {
      setLoading(false);
    }
  };

  const deleteReport = async (id: number) => {
    if (!confirm("Are you sure you want to delete this report?")) return;

    try {
      const response = await fetchWithAuth(`${API_ENDPOINTS.REPORTS}/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        setReports(reports.filter((r) => r.id !== id));
        if (selectedReport?.id === id) {
          setSelectedReport(null);
        }
      }
    } catch (error) {
      console.error("Failed to delete report:", error);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      fetchReports();
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  const excellentSites = reports.filter((r) => r.seo_score >= 80).length;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary shadow-lg">
              <TrendingUp className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">SiteSage</h1>
              <p className="text-xs text-muted-foreground">
                AI-Powered SEO Analyzer
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <ThemeToggle />
            <Button
              variant="ghost"
              size="icon"
              onClick={handleLogout}
              title="Sign out"
            >
              <LogOut className="h-[1.2rem] w-[1.2rem]" />
            </Button>
            <Button
              variant={viewMode === "grid" ? "default" : "outline"}
              size="sm"
              onClick={() => setViewMode("grid")}
            >
              <LayoutGrid className="h-4 w-4" />
            </Button>
            <Button
              variant={viewMode === "table" ? "default" : "outline"}
              size="sm"
              onClick={() => setViewMode("table")}
            >
              <List className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <URLForm onAnalysisComplete={fetchReports} />

            {/* Stats Cards */}
            <div className="grid grid-cols-2 gap-4">
              <Card className="p-4 border-primary/20 bg-primary/5">
                <div className="text-3xl font-bold text-primary">
                  {reports.length}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  Total Reports
                </div>
              </Card>
              <Card className="p-4 border-green-200 bg-green-50 dark:bg-green-950/20 dark:border-green-800">
                <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                  {excellentSites}
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  Excellent Sites
                </div>
              </Card>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-2">
            <div className="mb-6">
              <h2 className="text-3xl font-bold mb-2">Recent Reports</h2>
              <p className="text-muted-foreground">
                {reports.length}{" "}
                {reports.length === 1 ? "analysis" : "analyses"} completed
              </p>
            </div>

            {loading ? (
              <Card className="p-12 text-center">
                <div className="flex flex-col items-center gap-4">
                  <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent" />
                  <p className="text-muted-foreground">Loading reports...</p>
                </div>
              </Card>
            ) : reports.length === 0 ? (
              <Card className="p-12 text-center">
                <div className="flex flex-col items-center gap-4">
                  <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center">
                    <CheckCircle2 className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">
                      No reports yet
                    </h3>
                    <p className="text-muted-foreground max-w-sm mx-auto">
                      Start by analyzing your first website URL to get
                      comprehensive SEO insights
                    </p>
                  </div>
                </div>
              </Card>
            ) : viewMode === "grid" ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reports.map((report) => (
                  <ReportCard
                    key={report.id}
                    report={report}
                    onClick={() => setSelectedReport(report)}
                    onDelete={() => deleteReport(report.id)}
                  />
                ))}
              </div>
            ) : (
              <Card>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="border-b bg-muted/50">
                      <tr>
                        <th className="text-left py-3 px-4 font-semibold">
                          URL
                        </th>
                        <th className="text-center py-3 px-4 font-semibold">
                          Score
                        </th>
                        <th className="text-center py-3 px-4 font-semibold">
                          Load Time
                        </th>
                        <th className="text-center py-3 px-4 font-semibold">
                          Issues
                        </th>
                        <th className="text-center py-3 px-4 font-semibold">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {reports.map((report) => (
                        <tr
                          key={report.id}
                          onClick={() => setSelectedReport(report)}
                          className="border-b hover:bg-muted/50 cursor-pointer transition-colors"
                        >
                          <td className="py-3 px-4">
                            <div className="max-w-xs truncate font-medium">
                              {report.url}
                            </div>
                          </td>
                          <td className="py-3 px-4 text-center">
                            <span
                              className={`inline-flex items-center justify-center w-12 h-12 rounded-lg font-bold ${
                                report.seo_score >= 80
                                  ? "bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-400"
                                  : report.seo_score >= 60
                                  ? "bg-yellow-100 text-yellow-700 dark:bg-yellow-950 dark:text-yellow-400"
                                  : "bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-400"
                              }`}
                            >
                              {report.seo_score}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-center text-muted-foreground">
                            {report.metrics.load_time
                              ? `${report.metrics.load_time}s`
                              : "N/A"}
                          </td>
                          <td className="py-3 px-4 text-center">
                            {report.metrics.missing_alt_tags > 0 && (
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-400">
                                {report.metrics.missing_alt_tags} alt tags
                              </span>
                            )}
                          </td>
                          <td className="py-3 px-4 text-center">
                            <Button
                              variant="ghost"
                              size="icon"
                              className="text-muted-foreground hover:text-destructive"
                              onClick={(e) => {
                                e.stopPropagation();
                                deleteReport(report.id);
                              }}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            )}
          </div>
        </div>
      </main>

      {/* Report Detail Modal */}
      {selectedReport && (
        <ReportDetail
          report={selectedReport}
          onClose={() => setSelectedReport(null)}
        />
      )}
    </div>
  );
}
