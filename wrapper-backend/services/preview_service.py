from pathlib import Path
import markdown2
from typing import Optional
from fastapi import HTTPException

from wrapper_backend.utils.security import validate_file_path

class PreviewService:
    def __init__(self, applications_dir: Path):
        self.applications_dir = Path(applications_dir)

    def markdown_to_html(self, project_id: str, filename: str) -> Optional[str]:
        """Convert markdown file to HTML"""
        project_path = self.applications_dir / project_id

        # Validate file path to prevent path traversal attacks
        try:
            md_file = validate_file_path(project_path, filename, allow_dirs=False)
        except HTTPException:
            return None

        if not md_file.exists():
            return None

        markdown_content = md_file.read_text(encoding='utf-8')

        # Convert markdown to HTML with extras
        html_content = markdown2.markdown(
            markdown_content,
            extras=['fenced-code-blocks', 'tables', 'header-ids']
        )

        # Wrap in complete HTML document with styling
        html_with_style = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            color: #333;
        }}
        h1 {{ border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #eee; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ margin-top: 20px; }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 20px;
            margin-left: 0;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
        return html_with_style

    def get_pdf_path(self, project_id: str, filename: str) -> Optional[Path]:
        """Get path to PDF file if it exists"""
        project_path = self.applications_dir / project_id

        # Validate file path to prevent path traversal attacks
        try:
            pdf_file = validate_file_path(project_path, filename, allow_dirs=False)
        except HTTPException:
            return None

        if pdf_file.exists() and pdf_file.suffix == '.pdf':
            return pdf_file
        return None
