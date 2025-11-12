import api from './api';

export const createProject = async (institution, position, date) => {
  const response = await api.post('/api/projects', {
    institution,
    position,
    date,
  });
  return response.data;
};

export const listProjects = async () => {
  const response = await api.get('/api/projects');
  return response.data;
};
