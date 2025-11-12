import { useState, useEffect } from 'react';
import { listProjects, createProject } from '../services/projectService';

function ProjectDashboard({ onSelectProject }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    institution: '',
    position: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await listProjects();
      setProjects(data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    try {
      const newProject = await createProject(
        formData.institution,
        formData.position,
        formData.date
      );
      setProjects([newProject, ...projects]);
      setShowCreateForm(false);
      setFormData({ institution: '', position: '', date: new Date().toISOString().split('T')[0] });
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  if (loading) return <div>Loading projects...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Job Applications</h1>
        <button onClick={() => setShowCreateForm(!showCreateForm)}>
          {showCreateForm ? 'Cancel' : 'New Project'}
        </button>
      </div>

      {showCreateForm && (
        <form onSubmit={handleCreateProject} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc' }}>
          <div style={{ marginBottom: '10px' }}>
            <label>Institution:</label>
            <input
              type="text"
              value={formData.institution}
              onChange={(e) => setFormData({ ...formData, institution: e.target.value })}
              required
              style={{ marginLeft: '10px', padding: '5px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Position:</label>
            <input
              type="text"
              value={formData.position}
              onChange={(e) => setFormData({ ...formData, position: e.target.value })}
              required
              style={{ marginLeft: '10px', padding: '5px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label>Date:</label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              required
              style={{ marginLeft: '10px', padding: '5px' }}
            />
          </div>
          <button type="submit">Create Project</button>
        </form>
      )}

      <div>
        {projects.length === 0 ? (
          <p>No projects yet. Create your first job application project!</p>
        ) : (
          <div style={{ display: 'grid', gap: '15px' }}>
            {projects.map((project) => (
              <div
                key={project.project_id}
                onClick={() => onSelectProject(project)}
                style={{
                  padding: '15px',
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  '&:hover': { backgroundColor: '#f5f5f5' }
                }}
              >
                <h3>{project.institution} - {project.position}</h3>
                <p>Status: {project.current_stage}</p>
                <p>Updated: {new Date(project.updated_at).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProjectDashboard;
