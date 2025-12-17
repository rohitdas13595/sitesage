from typing import Dict, Any, List
import google.generativeai as genai
from app.config import get_settings
import json

settings = get_settings()


class AIInsightGenerator:
    """Generate SEO insights using Gemini when configured, otherwise fall back to heuristics."""
    
    def __init__(self):
        self.model = None
        if settings.GOOGLE_API_KEY:
            try:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.model = genai.GenerativeModel(settings.LLM_MODEL)
            except Exception as e:
                print(f"Warning: Gemini init failed; falling back to non-AI insights. ({e})")
    
    async def generate_insights(
        self,
        url: str,
        seo_score: float,
        analysis: Dict[str, Any],
        issues: List[str]
    ) -> Dict[str, Any]:
        """
        Turn the raw analysis output into a short summary and a handful of actionable suggestions.
        """
        if not self.model:
            return self._generate_fallback_insights(url, seo_score, analysis, issues)
        
        try:
            prompt = self._create_prompt(url, seo_score, analysis, issues)
            
            # Ask Gemini for a JSON-shaped response so it's easy to consume.
            response = self.model.generate_content(prompt)
            
            # Best effort: parse JSON, otherwise fall back to simple text parsing.
            insights = self._parse_ai_response(response.text)
            return insights
            
        except Exception as e:
            print(f"Error generating AI insights with Gemini; using fallback. ({e})")
            return self._generate_fallback_insights(url, seo_score, analysis, issues)
    
    def _create_prompt(
        self,
        url: str,
        seo_score: float,
        analysis: Dict[str, Any],
        issues: List[str]
    ) -> str:
        """Build a prompt for the LLM based on computed metrics + detected issues."""
        issues_text = "\n".join(f"- {issue}" for issue in issues) if issues else "No major issues found"
        
        prompt = f"""
Analyze the following SEO audit results for {url}:

SEO Score: {seo_score}/100

Key Metrics:
- Title: {analysis.get('title', 'N/A')}
- Meta Description: {analysis.get('meta_description', 'N/A')}
- H1 Tags: {analysis.get('h1_count', 0)}
- H2 Tags: {analysis.get('h2_count', 0)}
- Images: {analysis.get('image_count', 0)}
- Word Count: {analysis.get('word_count', 0)}
- Load Time: {analysis.get('load_time', 0)}s

Issues Identified:
{issues_text}

Please provide:
1. A 2-3 paragraph summary of the site's SEO quality
2. 3-5 specific, actionable improvement suggestions

Format your response as JSON with keys "summary" and "suggestions" (array of strings).
"""
        return prompt
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse the model output into `{summary, suggestions}`."""
        try:
            # Prefer JSON if the model returned it.
            if '{' in response and '}' in response:
                start = response.index('{')
                end = response.rindex('}') + 1
                json_str = response[start:end]
                data = json.loads(json_str)
                
                return {
                    'summary': data.get('summary', ''),
                    'suggestions': data.get('suggestions', [])
                }
        except:
            pass
        
        # Fallback: scrape suggestions out of a plain-text response.
        lines = response.strip().split('\n')
        summary_lines = []
        suggestions = []
        in_suggestions = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if 'suggestion' in line.lower() or line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '*')):
                in_suggestions = True
                # Clean up common list prefixes.
                cleaned = line.lstrip('0123456789.-* ')
                if cleaned:
                    suggestions.append(cleaned)
            elif not in_suggestions:
                summary_lines.append(line)
        
        return {
            'summary': ' '.join(summary_lines),
            'suggestions': suggestions[:5]  # Limit to 5 suggestions
        }
    
    def _generate_fallback_insights(
        self,
        url: str,
        seo_score: float,
        analysis: Dict[str, Any],
        issues: List[str]
    ) -> Dict[str, Any]:
        """Generate a decent summary/suggestions set without calling an LLM."""
        
        # Quick summary based on score buckets.
        if seo_score >= 80:
            summary = f"The website {url} demonstrates strong SEO fundamentals with a score of {seo_score}/100. "
            summary += "Most critical SEO elements are properly implemented. "
        elif seo_score >= 60:
            summary = f"The website {url} has a moderate SEO score of {seo_score}/100. "
            summary += "There are several areas that need attention to improve search engine visibility. "
        else:
            summary = f"The website {url} has significant SEO issues with a score of {seo_score}/100. "
            summary += "Immediate action is required to improve search engine rankings. "
        
        if issues:
            summary += f"Key issues include: {', '.join(issues[:3])}."
        
        # Suggestions based on the issues we detected.
        suggestions = []
        
        if any('title' in issue.lower() for issue in issues):
            suggestions.append("Optimize your page title to be between 30-60 characters and include target keywords")
        
        if any('meta description' in issue.lower() for issue in issues):
            suggestions.append("Add a compelling meta description of 120-160 characters to improve click-through rates")
        
        if any('h1' in issue.lower() for issue in issues):
            suggestions.append("Ensure each page has exactly one H1 tag that clearly describes the page content")
        
        if any('alt' in issue.lower() for issue in issues):
            suggestions.append("Add descriptive alt text to all images for better accessibility and SEO")
        
        if any('load time' in issue.lower() for issue in issues):
            suggestions.append("Optimize page load speed by compressing images, minifying CSS/JS, and leveraging browser caching")
        
        # Top up with generic suggestions if we don't have enough signal.
        generic_suggestions = [
            "Improve internal linking structure to help search engines discover content",
            "Create high-quality, original content that provides value to users",
            "Ensure mobile responsiveness and fast loading on all devices",
            "Build quality backlinks from reputable websites in your industry"
        ]
        
        while len(suggestions) < 5:
            for suggestion in generic_suggestions:
                if suggestion not in suggestions:
                    suggestions.append(suggestion)
                    if len(suggestions) >= 5:
                        break
        
        return {
            'summary': summary,
            'suggestions': suggestions[:5]
        }
