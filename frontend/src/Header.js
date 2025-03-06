import React from 'react';
import './Header.css'; // header style
import logo from './logo.png'; // logo

const Header = () => {
  return (
    <div className="header-container">
      <img src={logo} alt="Logo" className="header-logo" />
      <div className="header-text">Spartan Light Metal Products Makerspace</div>
    </div>
  );
};

export default Header;
