import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import api from '../services/api';

function ChatInterface({ project, wsRef }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [currentStreamingId, setCurrentStreamingId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Suggestion chips for common actions
  const suggestions = [
    { label: "Analyze job description", value: "analyze the job description" },
    { label: "Align my resume", value: "align my resume to this job" },
    { label: "Draft cover letter", value: "write a cover letter for this position" },
    { label: "Format resume", value: "format my resume" },
    { label: "Show project status", value: "what's the status of this project?" }
  ];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Listen to WebSocket for chat streaming
  useEffect(() => {
    if (!wsRef?.current) return;

    const ws = wsRef.current;
    const originalOnMessage = ws.onmessage;

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case 'chat_start':
          handleChatStart(message);
          break;

        case 'chat_token':
          handleChatToken(message);
          break;

        case 'chat_complete':
          handleChatComplete(message);
          break;

        case 'chat_error':
          handleChatError(message);
          break;

        default:
          // Pass to original handler for non-chat messages
          if (originalOnMessage) {
            originalOnMessage(event);
          }
      }
    };

    return () => {
      ws.onmessage = originalOnMessage;
    };
  }, [wsRef, messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleChatStart = (wsMessage) => {
    const { message_id, intent } = wsMessage;
    setCurrentStreamingId(message_id);

    // Add AI response message (initially empty, will stream in)
    const aiMessage = {
      id: message_id,
      role: 'assistant',
      content: '',
      intent: intent,
      streaming: true,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, aiMessage]);
  };

  const handleChatToken = (wsMessage) => {
    const { message_id, token } = wsMessage;

    setMessages(prev => prev.map(msg =>
      msg.id === message_id
        ? { ...msg, content: msg.content + token }
        : msg
    ));
  };

  const handleChatComplete = (wsMessage) => {
    const { message_id, usage } = wsMessage;

    setMessages(prev => prev.map(msg =>
      msg.id === message_id
        ? { ...msg, streaming: false, usage }
        : msg
    ));

    setCurrentStreamingId(null);
    setIsSending(false);
  };

  const handleChatError = (wsMessage) => {
    const { message_id, error } = wsMessage;

    setMessages(prev => prev.map(msg =>
      msg.id === message_id
        ? { ...msg, content: `Error: ${error}`, streaming: false, error: true }
        : msg
    ));

    setCurrentStreamingId(null);
    setIsSending(false);
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || isSending) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsSending(true);

    try {
      await api.post('/api/chat/message', {
        project_id: project.project_id,
        message: messageText,
        context: {
          institution: project.institution,
          position: project.position,
          stage: project.current_stage
        }
      });

      // Response will come via WebSocket
    } catch (error) {
      console.error('Failed to send message:', error);

      // Add error message
      setMessages(prev => [...prev, {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        error: true,
        timestamp: new Date().toISOString()
      }]);

      setIsSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion.value);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      backgroundColor: '#f9fafb'
    }}>
      {/* Messages Area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        {messages.length === 0 && (
          <div style={{
            textAlign: 'center',
            padding: '40px 20px',
            color: '#6b7280'
          }}>
            <h3 style={{ marginBottom: '10px', color: '#374151' }}>
              Welcome to {project.institution}
            </h3>
            <p style={{ marginBottom: '20px' }}>
              I can help you with job analysis, resume alignment, and cover letter drafting.
            </p>
            <p style={{ fontSize: '14px' }}>
              Try one of the suggestions below or type your own request.
            </p>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start'
            }}
          >
            <div style={{
              maxWidth: '75%',
              padding: '12px 16px',
              borderRadius: '12px',
              backgroundColor: msg.role === 'user'
                ? '#3b82f6'
                : msg.error
                  ? '#fef2f2'
                  : '#ffffff',
              color: msg.role === 'user'
                ? '#ffffff'
                : msg.error
                  ? '#dc2626'
                  : '#1f2937',
              boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
              position: 'relative'
            }}>
              {/* Intent badge for AI messages */}
              {msg.role === 'assistant' && msg.intent && msg.intent.skill !== 'conversational' && (
                <div style={{
                  fontSize: '11px',
                  color: '#6b7280',
                  marginBottom: '6px',
                  fontStyle: 'italic'
                }}>
                  Running: {msg.intent.skill}
                </div>
              )}

              {/* Message content */}
              <div style={{
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                lineHeight: '1.5'
              }}>
                {msg.content}
                {msg.streaming && (
                  <span style={{
                    animation: 'blink 1s infinite',
                    marginLeft: '2px'
                  }}>▊</span>
                )}
              </div>

              {/* Usage stats for AI messages */}
              {msg.role === 'assistant' && msg.usage && !msg.streaming && (
                <div style={{
                  fontSize: '10px',
                  color: '#9ca3af',
                  marginTop: '6px',
                  display: 'flex',
                  gap: '10px'
                }}>
                  <span>{msg.usage.input_tokens} in</span>
                  <span>{msg.usage.output_tokens} out</span>
                </div>
              )}

              {/* Copy button for AI messages */}
              {msg.role === 'assistant' && !msg.streaming && !msg.error && (
                <button
                  onClick={() => copyToClipboard(msg.content)}
                  style={{
                    position: 'absolute',
                    top: '8px',
                    right: '8px',
                    background: 'rgba(0, 0, 0, 0.05)',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '4px 8px',
                    fontSize: '11px',
                    cursor: 'pointer',
                    opacity: 0.7
                  }}
                  onMouseEnter={(e) => e.target.style.opacity = 1}
                  onMouseLeave={(e) => e.target.style.opacity = 0.7}
                >
                  Copy
                </button>
              )}
            </div>

            {/* Timestamp */}
            <div style={{
              fontSize: '11px',
              color: '#9ca3af',
              marginTop: '4px',
              paddingLeft: msg.role === 'user' ? '0' : '16px',
              paddingRight: msg.role === 'user' ? '16px' : '0'
            }}>
              {formatTimestamp(msg.timestamp)}
            </div>
          </div>
        ))}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggestion Chips (show when empty or not sending) */}
      {(messages.length === 0 || !isSending) && (
        <div style={{
          padding: '10px 20px',
          display: 'flex',
          gap: '8px',
          flexWrap: 'wrap',
          borderTop: '1px solid #e5e7eb'
        }}>
          {suggestions.map((suggestion, idx) => (
            <button
              key={idx}
              onClick={() => handleSuggestionClick(suggestion)}
              disabled={isSending}
              style={{
                padding: '8px 16px',
                borderRadius: '20px',
                border: '1px solid #d1d5db',
                backgroundColor: '#ffffff',
                color: '#374151',
                fontSize: '13px',
                cursor: isSending ? 'not-allowed' : 'pointer',
                opacity: isSending ? 0.5 : 1,
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => {
                if (!isSending) {
                  e.target.style.backgroundColor = '#f3f4f6';
                  e.target.style.borderColor = '#9ca3af';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = '#ffffff';
                e.target.style.borderColor = '#d1d5db';
              }}
            >
              {suggestion.label}
            </button>
          ))}
        </div>
      )}

      {/* Input Area */}
      <div style={{
        padding: '16px 20px',
        borderTop: '1px solid #e5e7eb',
        backgroundColor: '#ffffff'
      }}>
        <div style={{
          display: 'flex',
          gap: '12px',
          alignItems: 'flex-end'
        }}>
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isSending ? "Sending..." : "Type your message... (Shift+Enter for new line)"}
            disabled={isSending}
            style={{
              flex: 1,
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #d1d5db',
              fontSize: '14px',
              fontFamily: 'inherit',
              resize: 'none',
              minHeight: '44px',
              maxHeight: '120px',
              outline: 'none'
            }}
            rows={1}
          />
          <button
            onClick={() => handleSendMessage(inputValue)}
            disabled={!inputValue.trim() || isSending}
            style={{
              padding: '12px 24px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: (!inputValue.trim() || isSending) ? '#d1d5db' : '#3b82f6',
              color: '#ffffff',
              fontSize: '14px',
              fontWeight: '500',
              cursor: (!inputValue.trim() || isSending) ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseEnter={(e) => {
              if (inputValue.trim() && !isSending) {
                e.target.style.backgroundColor = '#2563eb';
              }
            }}
            onMouseLeave={(e) => {
              if (inputValue.trim() && !isSending) {
                e.target.style.backgroundColor = '#3b82f6';
              }
            }}
          >
            {isSending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>

      {/* CSS for blinking cursor animation */}
      <style>{`
        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }
      `}</style>
    </div>
  );
}

ChatInterface.propTypes = {
  project: PropTypes.shape({
    project_id: PropTypes.string.isRequired,
    institution: PropTypes.string.isRequired,
    position: PropTypes.string.isRequired,
    current_stage: PropTypes.string.isRequired
  }).isRequired,
  wsRef: PropTypes.object.isRequired
};

export default ChatInterface;
