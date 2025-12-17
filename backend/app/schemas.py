from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class URLSubmission(BaseModel):
    """Schema for URL submission"""
    url: HttpUrl
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com"
            }
        }


class BatchURLSubmission(BaseModel):
    """Schema for batch URL submission"""
    urls: List[HttpUrl] = Field(..., min_length=1, max_length=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "urls": ["https://example.com", "https://example.org"]
            }
        }


class SEOMetrics(BaseModel):
    """SEO metrics extracted from a page"""
    title: Optional[str] = None
    meta_description: Optional[str] = None
    h1_tags: List[str] = []
    h2_tags: List[str] = []
    images: List[Dict[str, Any]] = []
    load_time: Optional[float] = None
    missing_alt_tags: int = 0
    broken_links: int = 0
    accessibility: Dict[str, Any] = {}
    
    # Lighthouse Metrics
    performance_score: Optional[float] = None
    accessibility_score: Optional[float] = None
    best_practices_score: Optional[float] = None
    lighthouse_seo_score: Optional[float] = None


class AIInsights(BaseModel):
    """AI-generated insights"""
    summary: str
    suggestions: List[str]


class SEOReportResponse(BaseModel):
    """Complete SEO report response"""
    id: int
    url: str
    seo_score: float
    metrics: SEOMetrics
    ai_insights: Optional[AIInsights] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class SEOReportList(BaseModel):
    """List of SEO reports"""
    reports: List[SEOReportResponse]
    total: int
    page: int
    page_size: int


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    database: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None


class User(UserBase):
    id: int
    full_name: Optional[str] = None
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True

