import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { API_URL } from './config.js';
import './styles.css';

const savedTheme = window.localStorage.getItem('amaury-automation-theme');
document.documentElement.dataset.theme = savedTheme === 'light' ? 'light' : 'dark';

// wake do Render para acesso - Amaury
// O plano Free do Render hiberna sem uso; este aviso acorda a API assim que o portal abre.
// no-cors: a resposta não é lida, só importa que a requisição chegue ao serviço.
fetch(`${API_URL}/saude`, { mode: 'no-cors', cache: 'no-store' }).catch(() => {});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
