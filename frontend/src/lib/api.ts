// Base API URL (set `NEXT_PUBLIC_API_URL` to point at your backend)
export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Centralized endpoints so components don't hardcode paths.
export const API_ENDPOINTS = {
  ANALYZE: `${API_URL}/api/v1/seo/analyze`,
  ANALYZE_BATCH: `${API_URL}/api/v1/seo/analyze/batch`,
  REPORTS: `${API_URL}/api/v1/seo/reports`,
  HEALTH: `${API_URL}/health`,
};

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem("token");
  const headers = {
    ...options.headers,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }

  return response;
}
