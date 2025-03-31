import React from 'react';
import './ErrorBanner.css';

const ErrorBanner = ({ timestamp }) => {
  return (
    <div className="error-banner">
      <div className="error-content">
        <h2>Error Retrieving Data</h2>
        <p>An error occurred while attempting to retrieve data from the server.</p>
        <p>Please contact:</p>
        <ul>
          <li><a href="mailto:esergio@wustl.edu">esergio@wustl.edu</a></li>
          <li><a href="mailto:nwells@wustl.edu">nwells@wustl.edu</a></li>
        </ul>
        <p>Error Timestamp: {timestamp}</p>
      </div>
    </div>
  );
};

export default ErrorBanner;