import { useState } from 'react';
import api from '../services/api';

function FileUpload({ projectId, onUploadComplete }) {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = async (files) => {
    if (!files || files.length === 0) return;

    setUploading(true);
    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        await api.post(`/api/files/upload/${projectId}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      if (onUploadComplete) onUploadComplete();
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      style={{
        border: `2px dashed ${dragOver ? '#007bff' : '#ccc'}`,
        borderRadius: '5px',
        padding: '40px',
        textAlign: 'center',
        backgroundColor: dragOver ? '#f0f8ff' : 'white',
        cursor: 'pointer'
      }}
    >
      {uploading ? (
        <p>Uploading...</p>
      ) : (
        <>
          <p>Drag and drop files here, or click to select</p>
          <input
            type="file"
            multiple
            onChange={(e) => handleFileSelect(e.target.files)}
            style={{ display: 'none' }}
            id="file-input"
          />
          <label htmlFor="file-input" style={{ cursor: 'pointer', color: '#007bff' }}>
            Select Files
          </label>
        </>
      )}
    </div>
  );
}

export default FileUpload;
