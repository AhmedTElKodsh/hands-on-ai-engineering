import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import os

def convert_md_to_pdf(md_file_path, pdf_file_path):
    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to basic HTML
    html_content = markdown.markdown(md_content)

    # Initialize the PDF document
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom style for better readability
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10,
        alignment=TA_LEFT
    )

    story = []
    
    # Process lines to create story elements
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            story.append(Paragraph(line[2:], styles['Title']))
            story.append(Spacer(1, 12))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], styles['Heading1']))
            story.append(Spacer(1, 10))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['Heading2']))
            story.append(Spacer(1, 8))
        elif line.startswith('- '):
            story.append(Paragraph(line, custom_style))
        elif line.strip() == '':
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(line, custom_style))

    # Build the PDF
    doc.build(story)
    print(f"Successfully converted {md_file_path} to {pdf_file_path}")

if __name__ == "__main__":
    md_path = r"D:\AI\Gentech\POCs\hands-on-ai-engineering\conductor\analysis-summary.md"
    pdf_path = r"D:\AI\Gentech\POCs\hands-on-ai-engineering\conductor\analysis-summary.pdf"
    convert_md_to_pdf(md_path, pdf_path)
