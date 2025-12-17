import pytest
from app.services.seo_analyzer import SEOAnalyzer


def test_seo_analyzer_basic():
    """Test basic SEO analysis"""
    analyzer = SEOAnalyzer()
    
    crawl_data = {
        'url': 'https://example.com',
        'title': 'Example Domain',
        'meta_description': 'This is an example domain for illustrative examples in documents.',
        'h1_tags': ['Example Domain'],
        'h2_tags': ['More Information'],
        'images': [
            {'src': 'image.jpg', 'alt': 'Example', 'has_alt': True}
        ],
        'word_count': 500,
        'load_time': 1.5
    }
    
    result = analyzer.analyze(crawl_data)
    
    assert 'seo_score' in result
    assert 'issues' in result
    assert 'analysis' in result
    assert result['seo_score'] >= 0
    assert result['seo_score'] <= 100


def test_seo_analyzer_missing_title():
    """Test analysis with missing title"""
    analyzer = SEOAnalyzer()
    
    crawl_data = {
        'url': 'https://example.com',
        'title': None,
        'meta_description': 'Description',
        'h1_tags': ['Heading'],
        'h2_tags': [],
        'images': [],
        'word_count': 300,
        'load_time': 2.0
    }
    
    result = analyzer.analyze(crawl_data)
    
    assert any('title' in issue.lower() for issue in result['issues'])
    assert result['seo_score'] < 100


def test_seo_analyzer_missing_alt_tags():
    """Test analysis with missing alt tags"""
    analyzer = SEOAnalyzer()
    
    crawl_data = {
        'url': 'https://example.com',
        'title': 'Good Title for SEO Purposes',
        'meta_description': 'A good meta description that is between 120 and 160 characters long for optimal SEO performance.',
        'h1_tags': ['Main Heading'],
        'h2_tags': ['Subheading'],
        'images': [
            {'src': 'image1.jpg', 'alt': '', 'has_alt': False},
            {'src': 'image2.jpg', 'alt': '', 'has_alt': False},
        ],
        'word_count': 500,
        'load_time': 1.5
    }
    
    result = analyzer.analyze(crawl_data)
    
    assert result['missing_alt_tags'] == 2
    assert any('alt' in issue.lower() for issue in result['issues'])
