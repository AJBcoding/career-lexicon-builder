#!/bin/bash
# Simple wrapper to convert .pages files to PDF

echo "🚀 Starting .pages to PDF conversion..."
echo ""

osascript convert_pages_to_pdf.applescript

echo ""
echo "Done! Check my_documents/converted/ for your PDFs."
