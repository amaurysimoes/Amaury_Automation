import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

const savedTheme = window.localStorage.getItem('amaury-automation-theme');
document.documentElement.dataset.theme = savedTheme === 'light' ? 'light' : 'dark';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
