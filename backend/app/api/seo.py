import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import (
    URLSubmission,
    BatchURLSubmission,
    SEOReportResponse,
    SEOReportList,
    SEOMetrics,
    AIInsights
)
from app.models import SEOReport, User
from app.services.crawler import WebCrawler
from app.services.seo_analyzer import SEOAnalyzer
from app.services.ai_service import AIInsightGenerator
from app.services.pdf_service import PDFGenerator
from app.services.performance_service import PerformanceService
from app import auth

router = APIRouter(prefix="/api/v1/seo", tags=["SEO Analysis"])

crawler = WebCrawler()
analyzer = SEOAnalyzer()
ai_service = AIInsightGenerator()
pdf_generator = PDFGenerator()
performance_service = PerformanceService()


def format_report_response(report: SEOReport) -> SEOReportResponse:
    """Helper to format SEOReport model into SEOReportResponse schema"""
    return SEOReportResponse(
        id=report.id,
        url=report.url,
        seo_score=report.seo_score,
        metrics=SEOMetrics(
            title=report.title,
            meta_description=report.meta_description,
            h1_tags=report.h1_tags or [],
            h2_tags=report.h2_tags or [],
            images=report.images or [],
            load_time=report.load_time,
            missing_alt_tags=report.missing_alt_tags,
            broken_links=report.broken_links,
            accessibility=report.accessibility or {},
            performance_score=report.performance_score,
            accessibility_score=report.accessibility_score,
            best_practices_score=report.best_practices_score,
            lighthouse_seo_score=report.lighthouse_seo_score
        ),
        ai_insights=AIInsights(
            summary=report.ai_summary or "",
            suggestions=report.ai_suggestions or []
        ) if report.ai_summary else None,
        created_at=report.created_at
    )


@router.post("/analyze", response_model=SEOReportResponse, status_code=201)
async def analyze_url(
    submission: URLSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Run an SEO analysis for a single URL and persist the report for the current user.
    """
    url = str(submission.url)
    
    # Run analysis concurrently
    crawl_task = crawler.crawl(url)
    lighthouse_task = performance_service.get_lighthouse_metrics(url)
    
    crawl_data, lighthouse_metrics = await asyncio.gather(crawl_task, lighthouse_task)
    
    if 'error' in crawl_data:
        raise HTTPException(status_code=400, detail=f"Failed to crawl URL: {crawl_data['error']}")
    
    # Analyze SEO
    analysis_result = analyzer.analyze(crawl_data)
    
    # Generate AI insights
    ai_insights = await ai_service.generate_insights(
        url=url,
        seo_score=analysis_result['seo_score'],
        analysis=analysis_result['analysis'],
        issues=analysis_result['issues']
    )
    
    # Create report in database
    report = SEOReport(
        url=url,
        title=crawl_data.get('title'),
        meta_description=crawl_data.get('meta_description'),
        h1_tags=crawl_data.get('h1_tags', []),
        h2_tags=crawl_data.get('h2_tags', []),
        images=crawl_data.get('images', []),
        load_time=crawl_data.get('load_time'),
        seo_score=analysis_result['seo_score'],
        missing_alt_tags=analysis_result['missing_alt_tags'],
        broken_links=analysis_result.get('broken_links_count', 0),
        accessibility=crawl_data.get('accessibility', {}),
        performance_score=lighthouse_metrics.get('performance'),
        accessibility_score=lighthouse_metrics.get('accessibility'),
        best_practices_score=lighthouse_metrics.get('best_practices'),
        lighthouse_seo_score=lighthouse_metrics.get('seo'),
        ai_summary=ai_insights['summary'],
        ai_suggestions=ai_insights['suggestions'],
        full_report={
            'crawl_data': crawl_data,
            'analysis': analysis_result,
            'ai_insights': ai_insights
        },
        user_id=current_user.id
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    # Format response
    return format_report_response(report)


@router.post("/analyze/batch", response_model=List[SEOReportResponse])
async def analyze_batch_urls(
    submission: BatchURLSubmission,

    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Analyze multiple URLs in one request (up to 10) and return the generated reports.
    """
    urls = [str(url) for url in submission.urls]
    
    # Crawl all URLs concurrently
    crawl_results = await crawler.crawl_batch(urls)
    
    reports = []
    
    for crawl_data in crawl_results:
        if 'error' in crawl_data:
            continue
        
        url = crawl_data['url']
        
        # Analyze SEO
        analysis_result = analyzer.analyze(crawl_data)
        
        # Generate AI insights
        ai_insights = await ai_service.generate_insights(
            url=url,
            seo_score=analysis_result['seo_score'],
            analysis=analysis_result['analysis'],
            issues=analysis_result['issues']
        )
        
        # Get lighthouse metrics (optional for batch to save time, but user asked for it)
        lighthouse_metrics = await performance_service.get_lighthouse_metrics(url)
        
        # Create report
        report = SEOReport(
            url=url,
            title=crawl_data.get('title'),
            meta_description=crawl_data.get('meta_description'),
            h1_tags=crawl_data.get('h1_tags', []),
            h2_tags=crawl_data.get('h2_tags', []),
            images=crawl_data.get('images', []),
            load_time=crawl_data.get('load_time'),
            seo_score=analysis_result['seo_score'],
            missing_alt_tags=analysis_result['missing_alt_tags'],
            broken_links=analysis_result.get('broken_links_count', 0),
            accessibility=crawl_data.get('accessibility', {}),
            performance_score=lighthouse_metrics.get('performance'),
            accessibility_score=lighthouse_metrics.get('accessibility'),
            best_practices_score=lighthouse_metrics.get('best_practices'),
            lighthouse_seo_score=lighthouse_metrics.get('seo'),
            ai_summary=ai_insights['summary'],
            ai_suggestions=ai_insights['suggestions'],
            full_report={
                'crawl_data': crawl_data,
                'analysis': analysis_result,
                'ai_insights': ai_insights
            },
            user_id=current_user.id
        )
        
        db.add(report)
        reports.append(report)
    
    db.commit()
    
    # Format responses
    return [format_report_response(report) for report in reports]


@router.get("/reports", response_model=SEOReportList)
async def get_reports(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Get paginated list of SEO reports
    """
    offset = (page - 1) * page_size
    
    total = db.query(SEOReport).filter(SEOReport.user_id == current_user.id).count()
    reports = db.query(SEOReport)\
        .filter(SEOReport.user_id == current_user.id)\
        .order_by(SEOReport.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    report_responses = [format_report_response(report) for report in reports]
    
    return SEOReportList(
        reports=report_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/reports/{report_id}", response_model=SEOReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Get a specific SEO report by ID
    """
    report = db.query(SEOReport).filter(SEOReport.id == report_id, SEOReport.user_id == current_user.id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return format_report_response(report)


@router.delete("/reports/{report_id}", status_code=204)
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Delete a specific SEO report
    """
    report = db.query(SEOReport).filter(SEOReport.id == report_id, SEOReport.user_id == current_user.id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    
    return None


@router.get("/reports/{report_id}/download")
async def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Download a specific SEO report as PDF
    """
    report = db.query(SEOReport).filter(SEOReport.id == report_id, SEOReport.user_id == current_user.id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    pdf_buffer = pdf_generator.generate_report_pdf(report)
    
    filename = f"report_{report_id}_{report.url.replace('https://', '').replace('http://', '').replace('/', '_')}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

