import React from 'react';
import { createRoot } from 'react-dom/client';  // React 18 syntax
import App from './App';
import './App.css';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
