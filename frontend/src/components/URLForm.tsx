"use client";

import { useState } from "react";
import { API_ENDPOINTS, fetchWithAuth } from "@/lib/api";
import { Button } from "@/components/ui/button";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Search,
  Loader2,
  AlertCircle,
  CheckCircle2,
  Sparkles,
} from "lucide-react";

import { Textarea } from "@/components/ui/textarea";

interface URLFormProps {
  onAnalysisComplete: () => void;
}

export default function URLForm({ onAnalysisComplete }: URLFormProps) {
  const [urls, setUrls] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    const urlList = urls
      .split(/[\n,]+/)
      .map((u) => u.trim())
      .filter((u) => u.length > 0);

    if (urlList.length === 0) {
      setError("Please enter at least one URL");
      setLoading(false);
      return;
    }

    try {
      const isBatch = urlList.length > 1;
      const endpoint = isBatch
        ? API_ENDPOINTS.ANALYZE + "/batch"
        : API_ENDPOINTS.ANALYZE;
      const body = isBatch ? { urls: urlList } : { url: urlList[0] };

      const response = await fetchWithAuth(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to analyze URL(s)");
      }

      setSuccess(true);
      setUrls("");
      onAnalysisComplete();

      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-purple-600">
            <Search className="h-4 w-4 text-white" />
          </div>
          <div>
            <CardTitle>Analyze Website</CardTitle>
            <CardDescription>
              Enter one or more URLs (separated by newline or comma)
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Textarea
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              placeholder="https://example.com&#10;https://another.com"
              required
              disabled={loading}
              className="min-h-[100px] rounded-lg resize-none"
            />
          </div>
          {/* ... rest of the form ... */}

          {error && (
            <div className="flex items-start gap-2 rounded-lg border border-destructive/50 bg-destructive/10 p-3">
              <AlertCircle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          {success && (
            <div className="flex items-start gap-2 rounded-lg border border-green-500/50 bg-green-50 dark:bg-green-950/20 p-3">
              <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-green-700 dark:text-green-400 font-medium">
                Analysis completed successfully!
              </p>
            </div>
          )}

          <Button type="submit" disabled={loading} className="w-full h-11">
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Analyze URL
              </>
            )}
          </Button>
        </form>

        {/* A couple of quick tips for first-time users */}
        <div className="mt-6 pt-6 border-t space-y-3">
          <p className="text-xs font-semibold text-muted-foreground">
            Quick Tips:
          </p>
          <ul className="space-y-2 text-xs text-muted-foreground">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="h-3 w-3 text-primary flex-shrink-0 mt-0.5" />
              <span>Enter any public website URL</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="h-3 w-3 text-primary flex-shrink-0 mt-0.5" />
              <span>Get instant SEO score & insights</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="h-3 w-3 text-primary flex-shrink-0 mt-0.5" />
              <span>AI-powered recommendations</span>
            </li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
