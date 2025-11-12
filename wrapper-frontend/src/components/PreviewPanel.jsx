import { useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import api from '../services/api';

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function PreviewPanel({ projectId, filename, type }) {
  const [previewType, setPreviewType] = useState(type || 'html');
  const [htmlContent, setHtmlContent] = useState('');
  const [pdfUrl, setPdfUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  useEffect(() => {
    if (!projectId || !filename) return;

    loadPreview();
  }, [projectId, filename, previewType]);

  const loadPreview = async () => {
    setLoading(true);
    setError(null);

    try {
      if (previewType === 'html') {
        // Fetch HTML preview
        const response = await api.get(`/api/preview/html/${projectId}/${filename}`);
        setHtmlContent(response.data);
      } else if (previewType === 'pdf') {
        // Set PDF URL for react-pdf
        setPdfUrl(`${api.defaults.baseURL}/api/preview/pdf/${projectId}/${filename}`);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load preview');
    } finally {
      setLoading(false);
    }
  };

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  if (!projectId || !filename) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
        Select a file to preview
      </div>
    );
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Preview type selector */}
      <div style={{ padding: '10px', borderBottom: '1px solid #ddd', display: 'flex', gap: '10px', alignItems: 'center' }}>
        <button
          onClick={() => setPreviewType('html')}
          style={{
            padding: '8px 16px',
            background: previewType === 'html' ? '#007bff' : '#f5f5f5',
            color: previewType === 'html' ? 'white' : '#333',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          HTML (Fast)
        </button>
        <button
          onClick={() => setPreviewType('pdf')}
          style={{
            padding: '8px 16px',
            background: previewType === 'pdf' ? '#007bff' : '#f5f5f5',
            color: previewType === 'pdf' ? 'white' : '#333',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          PDF (Accurate)
        </button>
        <span style={{ marginLeft: 'auto', fontSize: '14px', color: '#666' }}>
          {filename}
        </span>
      </div>

      {/* Preview content */}
      <div style={{ flex: 1, overflow: 'auto', background: '#f5f5f5' }}>
        {loading && (
          <div style={{ padding: '40px', textAlign: 'center' }}>
            Loading preview...
          </div>
        )}

        {error && (
          <div style={{ padding: '40px', textAlign: 'center', color: 'red' }}>
            {error}
          </div>
        )}

        {!loading && !error && previewType === 'html' && (
          <iframe
            srcDoc={htmlContent}
            style={{
              width: '100%',
              height: '100%',
              border: 'none',
              background: 'white'
            }}
            title="HTML Preview"
          />
        )}

        {!loading && !error && previewType === 'pdf' && pdfUrl && (
          <div style={{ padding: '20px', background: 'white', minHeight: '100%' }}>
            <Document
              file={pdfUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={<div style={{ textAlign: 'center' }}>Loading PDF...</div>}
              error={<div style={{ textAlign: 'center', color: 'red' }}>Failed to load PDF</div>}
            >
              <Page pageNumber={pageNumber} />
            </Document>

            {numPages && numPages > 1 && (
              <div style={{ marginTop: '10px', textAlign: 'center' }}>
                <button
                  onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
                  disabled={pageNumber <= 1}
                  style={{ margin: '0 5px', padding: '5px 10px' }}
                >
                  Previous
                </button>
                <span style={{ margin: '0 10px' }}>
                  Page {pageNumber} of {numPages}
                </span>
                <button
                  onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}
                  disabled={pageNumber >= numPages}
                  style={{ margin: '0 5px', padding: '5px 10px' }}
                >
                  Next
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default PreviewPanel;
