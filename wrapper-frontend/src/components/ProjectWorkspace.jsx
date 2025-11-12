import { useState } from 'react';
import FileUpload from './FileUpload';
import PreviewPanel from './PreviewPanel';
import api from '../services/api';

function ProjectWorkspace({ project, onBack }) {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleAnalyzeJob = async () => {
    setProcessing(true);
    try {
      const response = await api.post('/api/skills/invoke', {
        project_id: project.project_id,
        skill_name: 'job-description-analysis',
        prompt: 'Analyze the job posting and save the analysis as JSON'
      });
      setResult(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Failed to analyze job posting');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={onBack} style={{ marginBottom: '20px' }}>
        ← Back to Dashboard
      </button>

      <h2>{project.institution} - {project.position}</h2>
      <p>Status: {project.current_stage}</p>

      <div style={{ marginTop: '30px' }}>
        <h3>Upload Job Posting</h3>
        <FileUpload
          projectId={project.project_id}
          onUploadComplete={() => alert('File uploaded successfully')}
        />
      </div>

      <div style={{ marginTop: '30px' }}>
        <h3>Actions</h3>
        <button
          onClick={handleAnalyzeJob}
          disabled={processing}
          style={{ padding: '10px 20px' }}
        >
          {processing ? 'Analyzing...' : 'Analyze Job Posting'}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#f5f5f5' }}>
          <h3>Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      <div style={{ marginTop: '30px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', height: '600px' }}>
        <div>
          <h3>Files</h3>
          <div style={{ border: '1px solid #ddd', borderRadius: '5px', padding: '10px' }}>
            <button
              onClick={() => setSelectedFile('01-job-analysis.md')}
              style={{
                display: 'block',
                width: '100%',
                padding: '10px',
                marginBottom: '5px',
                textAlign: 'left',
                background: selectedFile === '01-job-analysis.md' ? '#e3f2fd' : 'white',
                border: '1px solid #ddd',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              01-job-analysis.md
            </button>
            <button
              onClick={() => setSelectedFile('02-fit-analysis.md')}
              style={{
                display: 'block',
                width: '100%',
                padding: '10px',
                marginBottom: '5px',
                textAlign: 'left',
                background: selectedFile === '02-fit-analysis.md' ? '#e3f2fd' : 'white',
                border: '1px solid #ddd',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              02-fit-analysis.md
            </button>
            <button
              onClick={() => setSelectedFile('03-cover-letter.md')}
              style={{
                display: 'block',
                width: '100%',
                padding: '10px',
                textAlign: 'left',
                background: selectedFile === '03-cover-letter.md' ? '#e3f2fd' : 'white',
                border: '1px solid #ddd',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              03-cover-letter.md
            </button>
          </div>
        </div>
        <div>
          <h3>Preview</h3>
          <div style={{ border: '1px solid #ddd', borderRadius: '5px', height: '100%' }}>
            <PreviewPanel
              projectId={project.project_id}
              filename={selectedFile}
              type="html"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProjectWorkspace;
