import React from "react";
import { useNavigate } from "react-router-dom";
import "./Homepage.css";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Welcome to Our Platform</h1>
      <p>Select an option to proceed:</p>
      <button className="button" onClick={() => navigate("/billing_site")}>
        Go to Billing Site
      </button>
      <button className="button" onClick={() => navigate("/sign_in")}>
        Go to Sign-In Page
      </button>
    </div>
  );
};

export default HomePage;