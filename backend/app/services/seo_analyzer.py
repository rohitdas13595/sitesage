from typing import Dict, Any, List



class SEOAnalyzer:
    """Analyze crawled data and compute SEO scores"""
    
    def __init__(self):
        self.max_score = 100
        
    def analyze(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze crawled data and generate SEO score
        
        Args:
            crawl_data: Data from web crawler
            
        Returns:
            Analysis results with SEO score
        """
        if 'error' in crawl_data:
            return {
                'seo_score': 0,
                'issues': [crawl_data['error']],
                'analysis': {}
            }
        
        issues = []
        score = self.max_score
        
        # Title analysis
        title_score, title_issues = self._analyze_title(crawl_data.get('title'))
        score += title_score
        issues.extend(title_issues)
        
        # Meta description analysis
        meta_score, meta_issues = self._analyze_meta_description(
            crawl_data.get('meta_description')
        )
        score += meta_score
        issues.extend(meta_issues)
        
        # Heading structure analysis
        h1_score, h1_issues = self._analyze_h1_tags(crawl_data.get('h1_tags', []))
        score += h1_score
        issues.extend(h1_issues)
        
        # Image analysis
        img_score, img_issues, missing_alts = self._analyze_images(
            crawl_data.get('images', [])
        )
        score += img_score
        issues.extend(img_issues)
        
        # Content analysis
        content_score, content_issues = self._analyze_content(
            crawl_data.get('word_count', 0)
        )
        score += content_score
        issues.extend(content_issues)
        
        # Performance analysis
        perf_score, perf_issues = self._analyze_performance(
            crawl_data.get('load_time', 0)
        )
        score += perf_score
        issues.extend(perf_issues)

        # Broken link analysis
        link_score, link_issues = self._analyze_links(
            crawl_data.get('broken_links_count', 0)
        )
        score += link_score
        issues.extend(link_issues)

        # Accessibility analysis
        acc_score, acc_issues = self._analyze_accessibility(
            crawl_data.get('accessibility', {})
        )
        score += acc_score
        issues.extend(acc_issues)
        
        # Ensure score is between 0 and 100
        final_score = max(0, min(100, score))
        
        return {
            'seo_score': round(final_score, 1),
            'issues': issues,
            'missing_alt_tags': missing_alts,
            'broken_links_count': crawl_data.get('broken_links_count', 0),
            'analysis': {
                'title': crawl_data.get('title'),
                'meta_description': crawl_data.get('meta_description'),
                'h1_count': len(crawl_data.get('h1_tags', [])),
                'h2_count': len(crawl_data.get('h2_tags', [])),
                'image_count': len(crawl_data.get('images', [])),
                'word_count': crawl_data.get('word_count', 0),
                'load_time': crawl_data.get('load_time', 0),
                'broken_links': crawl_data.get('broken_links_count', 0)
            }
        }
    
    def _analyze_title(self, title: str) -> tuple[int, List[str]]:
        """Analyze page title"""
        issues = []
        score = 0
        
        if not title:
            issues.append("Missing page title")
            score -= 15
        elif len(title) < 30:
            issues.append("Title is too short (< 30 characters)")
            score -= 10
        elif len(title) > 60:
            issues.append("Title is too long (> 60 characters)")
            score -= 5
        
        return score, issues
    
    def _analyze_meta_description(self, meta_desc: str) -> tuple[int, List[str]]:
        """Analyze meta description"""
        issues = []
        score = 0
        
        if not meta_desc:
            issues.append("Missing meta description")
            score -= 15
        elif len(meta_desc) < 120:
            issues.append("Meta description is too short (< 120 characters)")
            score -= 10
        elif len(meta_desc) > 160:
            issues.append("Meta description is too long (> 160 characters)")
            score -= 5
        
        return score, issues
    
    def _analyze_h1_tags(self, h1_tags: List[str]) -> tuple[int, List[str]]:
        """Analyze H1 tags"""
        issues = []
        score = 0
        
        if len(h1_tags) == 0:
            issues.append("No H1 tag found")
            score -= 15
        elif len(h1_tags) > 1:
            issues.append(f"Multiple H1 tags found ({len(h1_tags)})")
            score -= 10
        
        return score, issues
    
    def _analyze_images(self, images: List[Dict[str, Any]]) -> tuple[int, List[str], int]:
        """Analyze images and alt tags"""
        issues = []
        score = 0
        
        if not images:
            return score, issues, 0
        
        missing_alts = sum(1 for img in images if not img.get('has_alt', False))
        
        if missing_alts > 0:
            percentage = (missing_alts / len(images)) * 100
            issues.append(f"{missing_alts} images missing alt tags ({percentage:.1f}%)")
            score -= min(20, missing_alts * 2)
        
        return score, issues, missing_alts
    
    def _analyze_content(self, word_count: int) -> tuple[int, List[str]]:
        """Analyze content length"""
        issues = []
        score = 0
        
        if word_count < 300:
            issues.append(f"Low word count ({word_count} words)")
            score -= 10
        
        return score, issues
    
    def _analyze_performance(self, load_time: float) -> tuple[int, List[str]]:
        """Analyze page load performance"""
        issues = []
        score = 0
        
        if load_time > 3.0:
            issues.append(f"Slow page load time ({load_time}s)")
            score -= 15
        elif load_time > 2.0:
            issues.append(f"Page load time could be improved ({load_time}s)")
            score -= 5
        
        return score, issues

    def _analyze_links(self, broken_links_count: int) -> tuple[int, List[str]]:
        """Analyze broken links"""
        issues = []
        score = 0
        
        if broken_links_count > 0:
            issues.append(f"Found {broken_links_count} broken links")
            score -= min(20, broken_links_count * 5)
            
        return score, issues

    def _analyze_accessibility(self, accessibility: Dict[str, Any]) -> tuple[int, List[str]]:
        """Analyze accessibility metrics"""
        issues = []
        score = 0
        
        if not accessibility.get('has_lang'):
            issues.append("Missing 'lang' attribute on <html> tag")
            score -= 10
            
        missing_labels = accessibility.get('missing_labels_count', 0)
        if missing_labels > 0:
            issues.append(f"Found {missing_labels} interactive elements (links/buttons) without descriptive labels")
            score -= min(15, missing_labels * 3)
            
        return score, issues
