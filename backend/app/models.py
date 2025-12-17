from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SEOReport(Base):
    """SEO Report model for storing analysis results"""
    
    __tablename__ = "seo_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Metadata
    title = Column(String, nullable=True)
    meta_description = Column(Text, nullable=True)
    h1_tags = Column(JSON, nullable=True)  # List of H1 tags
    h2_tags = Column(JSON, nullable=True)  # List of H2 tags
    images = Column(JSON, nullable=True)   # List of image data
    
    # Metrics
    load_time = Column(Float, nullable=True)
    seo_score = Column(Float, nullable=True)
    missing_alt_tags = Column(Integer, default=0)
    broken_links = Column(Integer, default=0)
    accessibility = Column(JSON, nullable=True)  # Accessibility metrics
    
    # Lighthouse Metrics
    performance_score = Column(Float, nullable=True)
    accessibility_score = Column(Float, nullable=True)
    best_practices_score = Column(Float, nullable=True)
    lighthouse_seo_score = Column(Float, nullable=True)
    
    # AI Insights
    ai_summary = Column(Text, nullable=True)
    ai_suggestions = Column(JSON, nullable=True)  # List of suggestions
    
    # Full report data
    full_report = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="reports")
    
    def __repr__(self):
        return f"<SEOReport(id={self.id}, url={self.url}, score={self.seo_score})>"


class User(Base):
    """User model for authentication"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    reports = relationship("SEOReport", back_populates="owner")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
