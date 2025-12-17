import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import time
from urllib.parse import urljoin, urlparse


class WebCrawler:
    """Asynchronous web crawler for extracting SEO data"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        
    async def crawl(self, url: str) -> Dict[str, Any]:
        """
        Crawl a URL and extract SEO-relevant data
        
        Args:
            url: The URL to crawl
            
        Returns:
            Dictionary containing extracted data
        """
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    headers={'User-Agent': 'SiteSage/1.0 SEO Analyzer'}
                ) as response:
                    html = await response.text()
                    load_time = time.time() - start_time
                    
                    soup = BeautifulSoup(html, 'lxml')
                    
                    raw_links = self._extract_links(soup, url)
                    checked_links = await self._check_links(session, raw_links)
                    broken_links_count = sum(1 for link in checked_links if link.get('broken'))
                    accessibility = self._extract_accessibility_metrics(soup)

                    return {
                        'url': url,
                        'status_code': response.status,
                        'load_time': round(load_time, 2),
                        'title': self._extract_title(soup),
                        'meta_description': self._extract_meta_description(soup),
                        'h1_tags': self._extract_h1_tags(soup),
                        'h2_tags': self._extract_h2_tags(soup),
                        'images': self._extract_images(soup, url),
                        'links': checked_links,
                        'broken_links_count': broken_links_count,
                        'word_count': self._count_words(soup),
                        'accessibility': accessibility,
                    }
                    
        except asyncio.TimeoutError:
            return {'error': 'Request timeout', 'url': url}
        except Exception as e:
            return {'error': str(e), 'url': url}
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '').strip() if meta_desc else None
    
    def _extract_h1_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract all H1 tags"""
        return [h1.get_text().strip() for h1 in soup.find_all('h1')]
    
    def _extract_h2_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract all H2 tags"""
        return [h2.get_text().strip() for h2 in soup.find_all('h2')]
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Extract image data including alt tags"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src:
                images.append({
                    'src': urljoin(base_url, src),
                    'alt': img.get('alt', ''),
                    'has_alt': bool(img.get('alt', '').strip())
                })
        return images
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all links"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href:
                full_url = urljoin(base_url, href)
                links.append({
                    'url': full_url,
                    'text': link.get_text().strip(),
                    'is_external': urlparse(full_url).netloc != urlparse(base_url).netloc
                })
        return links
    
    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in the page content"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = text.split()
        return len(words)

    def _extract_accessibility_metrics(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract basic accessibility metrics"""
        html_tag = soup.find('html')
        lang = html_tag.get('lang') if html_tag else None
        
        # Check for buttons/links without text or aria-labels
        missing_labels = 0
        for tag in soup.find_all(['button', 'a']):
            text = tag.get_text().strip()
            aria_label = tag.get('aria-label')
            aria_labelledby = tag.get('aria-labelledby')
            
            if not text and not aria_label and not aria_labelledby:
                # For links, check if they contain an image with alt text
                if tag.name == 'a' and tag.find('img', alt=True):
                    continue
                missing_labels += 1
                
        return {
            'has_lang': bool(lang),
            'lang': lang,
            'missing_labels_count': missing_labels
        }
    
    async def _check_links(self, session: aiohttp.ClientSession, links: List[Dict[str, str]], limit: int = 20) -> List[Dict[str, Any]]:
        """Check for broken links (limit to avoid long wait times)"""
        checked_links = []
        # Filter for unique URLs to avoid checking same link twice
        unique_urls = list(set(link['url'] for link in links))[:limit]
        
        async def check_url(url):
            try:
                async with session.head(url, timeout=5, allow_redirects=True) as response:
                    return {'url': url, 'status': response.status, 'broken': response.status >= 400}
            except:
                try:
                    # Fallback to GET if HEAD fails (some servers block HEAD)
                    async with session.get(url, timeout=5) as response:
                        return {'url': url, 'status': response.status, 'broken': response.status >= 400}
                except:
                    return {'url': url, 'status': 0, 'broken': True}

        tasks = [check_url(url) for url in unique_urls]
        results = await asyncio.gather(*tasks)
        
        # Map results back to original links
        broken_map = {res['url']: res['broken'] for res in results}
        
        for link in links:
            is_broken = broken_map.get(link['url'], False)
            checked_links.append({
                **link,
                'broken': is_broken
            })
            
        return checked_links

    async def crawl_batch(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Crawl multiple URLs concurrently
        
        Args:
            urls: List of URLs to crawl
            
        Returns:
            List of crawl results
        """
        tasks = [self.crawl(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'url': urls[i],
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
