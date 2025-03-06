import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Homepage.css';

//main page
const HomePage = () => {
  const navigate = useNavigate();

  const goToBillingSite = () => {
    navigate('/billing_site'); // jump to /billing_site page
  };

  const goToSignIn = () => {
    navigate('/sign_in'); // jump to /sign_in page
  };

  return (
    <div className="home-container">
      <h1>Welcome to Our Platform</h1>
      <p>Select an option to proceed:</p>
      <button className="button" onClick={goToBillingSite}>
        Go to Billing Site
      </button>
      <button className="button" onClick={goToSignIn}>
        Go to Sign-In Page
      </button>
    </div>
  );
};

export default HomePage;
