import { useRef, useEffect } from 'react';

function StreamingDisplay({ content, isComplete, usage, title }) {
  const contentRef = useRef(null);

  useEffect(() => {
    if (contentRef.current && !isComplete) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [content, isComplete]);

  return (
    <div style={{
      marginTop: '20px',
      border: '1px solid #ddd',
      borderRadius: '5px',
      overflow: 'hidden'
    }}>
      <div style={{
        padding: '10px',
        backgroundColor: '#f8f8f8',
        borderBottom: '1px solid #ddd',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h4 style={{ margin: 0 }}>
          {title || (isComplete ? 'Complete' : 'Streaming...')}
          {!isComplete && <span className="spinner"> ⏳</span>}
        </h4>
        {usage && (
          <div style={{ fontSize: '12px', color: '#666' }}>
            <span>Input: {usage.input_tokens} </span>
            <span>Output: {usage.output_tokens}</span>
          </div>
        )}
      </div>

      <div
        ref={contentRef}
        style={{
          padding: '15px',
          backgroundColor: 'white',
          maxHeight: '400px',
          overflow: 'auto',
          whiteSpace: 'pre-wrap',
          fontFamily: 'monospace',
          fontSize: '13px',
          lineHeight: '1.5'
        }}
      >
        {content || <em style={{ color: '#999' }}>Waiting for output...</em>}
      </div>
    </div>
  );
}

export default StreamingDisplay;
