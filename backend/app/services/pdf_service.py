from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import io

class PDFGenerator:
    def generate_report_pdf(self, report):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("SiteSage SEO Report", styles['Title']))
        elements.append(Paragraph(f"URL: {report.url}", styles['Normal']))
        elements.append(Spacer(1, 24))

        # Score
        score_color = colors.green if report.seo_score >= 80 else (colors.orange if report.seo_score >= 60 else colors.red)
        score_style = styles['Heading2']
        elements.append(Paragraph(f'<font color="{score_color.hexval()}">Overall SEO Score: {report.seo_score}/100</font>', score_style))
        elements.append(Spacer(1, 12))

        # AI Summary
        elements.append(Paragraph("AI Analysis Summary", styles['Heading3']))
        elements.append(Paragraph(report.ai_summary or "No summary available.", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Suggestions
        if report.ai_suggestions:
            elements.append(Paragraph("Actionable Suggestions", styles['Heading3']))
            for suggestion in report.ai_suggestions:
                elements.append(Paragraph(f"• {suggestion}", styles['Normal']))
            elements.append(Spacer(1, 12))

        # Metrics Table
        elements.append(Paragraph("Detailed Metrics", styles['Heading3']))
        data = [
            ["Metric", "Value"],
            ["Title", report.title or "N/A"],
            ["Load Time", f"{report.load_time}s" if report.load_time else "N/A"],
            ["Broken Links", str(report.broken_links)],
            ["Missing Alt Tags", str(report.missing_alt_tags)],
            ["Lighthouse Performance", f"{report.performance_score:.1f}" if report.performance_score is not None else "N/A"],
            ["Lighthouse Accessibility", f"{report.accessibility_score:.1f}" if report.accessibility_score is not None else "N/A"],
            ["Lighthouse Best Practices", f"{report.best_practices_score:.1f}" if report.best_practices_score is not None else "N/A"],
            ["Lighthouse SEO", f"{report.lighthouse_seo_score:.1f}" if report.lighthouse_seo_score is not None else "N/A"]
        ]
        
        t = Table(data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(t)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
