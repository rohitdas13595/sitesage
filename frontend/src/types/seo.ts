export interface SEOMetrics {
  title: string | null;
  meta_description: string | null;
  h1_tags: string[];
  h2_tags: string[];
  images: Array<{
    src: string;
    alt: string;
    has_alt: boolean;
  }>;
  load_time: number | null;
  missing_alt_tags: number;
  broken_links: number;
  accessibility: {
    has_lang: boolean;
    lang: string | null;
    missing_labels_count: number;
  };
  performance_score: number | null;
  accessibility_score: number | null;
  best_practices_score: number | null;
  lighthouse_seo_score: number | null;
}

export interface AIInsights {
  summary: string;
  suggestions: string[];
}

export interface SEOReport {
  id: number;
  url: string;
  seo_score: number;
  metrics: SEOMetrics;
  ai_insights: AIInsights | null;
  created_at: string;
}

export interface SEOReportList {
  reports: SEOReport[];
  total: number;
  page: number;
  page_size: number;
}
