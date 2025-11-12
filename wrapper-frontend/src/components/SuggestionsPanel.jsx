import React, { useState, useEffect } from 'react';
import api from '../services/api';

function SuggestionsPanel({ project }) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSuggestions();
  }, [project.project_id]);

  const loadSuggestions = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/suggestions/${project.project_id}/next-steps`);
      setSuggestions(response.data.suggestions);
      setError(null);
    } catch (err) {
      setError('Failed to load suggestions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    // Execute suggested action
    if (suggestion.action.startsWith('run_skill:')) {
      const skillName = suggestion.action.split(':')[1];
      // Trigger skill invocation (integrate with existing handler)
      console.log('Running skill:', skillName);
      // TODO: Integrate with actual skill invocation
      alert(`Would run skill: ${skillName}\n\nIntegrate this with your existing skill invocation handler.`);
    } else if (suggestion.action === 'upload_file') {
      // Focus file upload component
      console.log('Focus upload');
      alert('Please use the File Upload section above to add your job posting.');
    } else if (suggestion.action === 'review') {
      alert('Review your completed documents in the preview panel.');
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading suggestions...</div>;
  }

  if (error) {
    return (
      <div style={styles.error}>
        {error}
        <button onClick={loadSuggestions} style={styles.retryButton}>
          Retry
        </button>
      </div>
    );
  }

  if (suggestions.length === 0) {
    return (
      <div style={styles.empty}>
        <p>No suggestions at this time.</p>
        <p>Keep working on your application!</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Smart Suggestions</h3>
      {suggestions.map((suggestion, index) => (
        <div
          key={index}
          style={{
            ...styles.suggestion,
            ...(suggestion.type === 'critical' ? styles.critical : {}),
            ...(suggestion.type === 'recommended' ? styles.recommended : {}),
            ...(suggestion.type === 'optional' ? styles.optional : {})
          }}
          onClick={() => handleSuggestionClick(suggestion)}
        >
          <div style={styles.suggestionHeader}>
            <span style={styles.suggestionTitle}>{suggestion.title}</span>
            <span style={styles.suggestionBadge}>{suggestion.type}</span>
          </div>
          <p style={styles.suggestionDescription}>{suggestion.description}</p>
          {suggestion.priority && (
            <span style={styles.priority}>Priority: {suggestion.priority}</span>
          )}
        </div>
      ))}
      <button onClick={loadSuggestions} style={styles.refreshButton}>
        Refresh Suggestions
      </button>
    </div>
  );
}

const styles = {
  container: {
    padding: '20px',
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    marginTop: '20px'
  },
  title: {
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '15px',
    color: '#333'
  },
  suggestion: {
    backgroundColor: 'white',
    padding: '15px',
    marginBottom: '10px',
    borderRadius: '6px',
    cursor: 'pointer',
    border: '1px solid #e0e0e0',
    transition: 'all 0.2s',
  },
  critical: {
    borderLeft: '4px solid #dc3545'
  },
  recommended: {
    borderLeft: '4px solid #007bff'
  },
  optional: {
    borderLeft: '4px solid #28a745'
  },
  suggestionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px'
  },
  suggestionTitle: {
    fontWeight: '600',
    fontSize: '14px',
    color: '#333'
  },
  suggestionBadge: {
    fontSize: '11px',
    padding: '2px 8px',
    borderRadius: '12px',
    backgroundColor: '#e0e0e0',
    color: '#666',
    textTransform: 'uppercase'
  },
  suggestionDescription: {
    fontSize: '13px',
    color: '#666',
    margin: '0 0 8px 0',
    lineHeight: '1.4'
  },
  priority: {
    fontSize: '11px',
    color: '#999'
  },
  refreshButton: {
    marginTop: '15px',
    padding: '8px 16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px'
  },
  loading: {
    padding: '20px',
    textAlign: 'center',
    color: '#666'
  },
  error: {
    padding: '20px',
    backgroundColor: '#fee',
    border: '1px solid #fcc',
    borderRadius: '4px',
    color: '#c33',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  retryButton: {
    padding: '6px 12px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px'
  },
  empty: {
    padding: '30px',
    textAlign: 'center',
    color: '#999',
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    marginTop: '20px'
  }
};

export default SuggestionsPanel;
