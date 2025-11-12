import { useState } from 'react';
import ProjectDashboard from './components/ProjectDashboard';

function App() {
  const [selectedProject, setSelectedProject] = useState(null);

  if (selectedProject) {
    return (
      <div>
        <button onClick={() => setSelectedProject(null)}>← Back to Dashboard</button>
        <h2>Project: {selectedProject.institution} - {selectedProject.position}</h2>
        <p>Project workspace coming soon...</p>
      </div>
    );
  }

  return <ProjectDashboard onSelectProject={setSelectedProject} />;
}

export default App;
