import { useState } from 'react';
import FileUpload from './FileUpload';
import api from '../services/api';

function ProjectWorkspace({ project, onBack }) {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

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
    </div>
  );
}

export default ProjectWorkspace;
