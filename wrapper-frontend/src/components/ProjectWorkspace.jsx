import { useState, useEffect, useRef } from 'react';
import FileUpload from './FileUpload';
import PreviewPanel from './PreviewPanel';
import api from '../services/api';

function ProjectWorkspace({ project, onBack }) {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [useAPI, setUseAPI] = useState(false);
  const [streaming, setStreaming] = useState('');
  const [streamComplete, setStreamComplete] = useState(false);
  const [usage, setUsage] = useState(null);
  const wsRef = useRef(null);
  const streamingRef = useRef(null);

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [project.project_id]);

  useEffect(() => {
    // Auto-scroll to bottom when streaming updates
    if (streamingRef.current && !streamComplete) {
      streamingRef.current.scrollTop = streamingRef.current.scrollHeight;
    }
  }, [streaming, streamComplete]);

  const connectWebSocket = () => {
    const wsUrl = `ws://localhost:8000/ws/${project.project_id}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case 'skill_start':
          setProcessing(true);
          setStreaming('');
          setStreamComplete(false);
          setUsage(null);
          break;

        case 'skill_token':
          // Append token to streaming content (API mode)
          setStreaming(prev => prev + message.token);
          break;

        case 'skill_output':
          // Append line output (CLI mode)
          setStreaming(prev => prev + message.output);
          break;

        case 'skill_complete':
          setProcessing(false);
          setStreamComplete(true);
          if (message.usage) {
            setUsage(message.usage);
          }
          break;

        case 'skill_error':
          setProcessing(false);
          setResult({ error: message.error });
          break;

        case 'file_created':
          console.log('New file created:', message.filename);
          break;
      }
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    wsRef.current.onclose = () => {
      console.log('WebSocket closed');
    };
  };

  const handleAnalyzeJob = async () => {
    setResult(null);
    setStreaming('');

    try {
      const response = await api.post('/api/skills/invoke', {
        project_id: project.project_id,
        skill_name: 'job-description-analysis',
        prompt: 'Analyze the job posting and save the analysis as JSON',
        stream: true,
        use_api: useAPI
      });

      // Response just confirms started
      console.log('Skill execution started:', response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Failed to start analysis');
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

        {/* API Mode Toggle */}
        <div style={{ marginBottom: '10px' }}>
          <label>
            <input
              type="checkbox"
              checked={useAPI}
              onChange={(e) => setUseAPI(e.target.checked)}
            />
            {' '}Use Anthropic API (faster, requires API key)
          </label>
        </div>

        <button
          onClick={handleAnalyzeJob}
          disabled={processing}
          style={{ padding: '10px 20px' }}
        >
          {processing ? 'Analyzing...' : 'Analyze Job Posting'}
        </button>

        {useAPI && (
          <span style={{ marginLeft: '10px', color: '#666', fontSize: '14px' }}>
            3-5x faster than CLI
          </span>
        )}
      </div>

      {/* Streaming Output */}
      {streaming && (
        <div style={{
          marginTop: '30px',
          padding: '15px',
          backgroundColor: '#f5f5f5',
          borderRadius: '5px',
          maxHeight: '400px',
          overflow: 'auto'
        }}
        ref={streamingRef}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <h3>
              {streamComplete ? 'Analysis Complete' : 'Analyzing...'}
              {processing && <span className="spinner"> ⏳</span>}
            </h3>
            {usage && (
              <span style={{ fontSize: '12px', color: '#666' }}>
                Tokens: {usage.input_tokens} in / {usage.output_tokens} out
              </span>
            )}
          </div>

          <div style={{
            whiteSpace: 'pre-wrap',
            fontFamily: 'monospace',
            fontSize: '13px',
            lineHeight: '1.5'
          }}>
            {streaming}
          </div>
        </div>
      )}

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
