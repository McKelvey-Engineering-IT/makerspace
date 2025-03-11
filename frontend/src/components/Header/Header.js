import React from 'react';
import './Header.css';
import logo from '../../media/logo.png'; 

const Header = () => {
  return (
    <div className="header-container">
      <img src={logo} alt="Logo" className="header-logo" />
      <div className="header-text">Spartan Light Metal Products Makerspace</div>
    </div>
  );
};

export default Header;
