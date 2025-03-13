import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './components/Homepage/Homepage';
import App from './App';
import { AppProvider } from './AppContext';
import './index.css';

const root = createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/sign_in" element={<App />} />
        </Routes>
      </BrowserRouter>
    </AppProvider>
  </React.StrictMode>
);