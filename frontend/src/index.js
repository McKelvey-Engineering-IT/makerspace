
import React from 'react';
// import ReactDOM from 'react-dom';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import HomePage from './Homepage';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        {/* default page */}
        <Route path="/" element={<HomePage />} />
        
        {/* /billing_site  
        <Route path="/billing_site" element={<BillingSite />} />*/}

        {/* /sign_in  */}
        <Route path="/sign_in" element={<App />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  // document.getElementById('root')
);
