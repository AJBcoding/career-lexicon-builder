import { useState, useEffect } from 'react';
import { healthCheck } from './services/api';

function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    healthCheck().then(setHealth).catch(console.error);
  }, []);

  return (
    <div>
      <h1>Career Lexicon Wrapper</h1>
      <p>Backend Status: {health?.status || 'connecting...'}</p>
    </div>
  );
}

export default App;
