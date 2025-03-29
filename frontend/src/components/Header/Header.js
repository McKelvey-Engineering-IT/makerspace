import React, { useContext } from 'react';
import { AppContext } from '../../AppContext';
import './Header.css';
import logo from '../../media/logo.png';
import { FaBell, FaBellSlash } from 'react-icons/fa';

const Header = () => {
  const { soundAlertsEnabled, setSoundAlertsEnabled } = useContext(AppContext);

  return (
    <div className="header-container">
      <img src={logo} alt="Logo" className="header-logo" />
      <div className="header-text">Spartan Light Metal Products Makerspace</div>
      <button 
        className="sound-toggle"
        onClick={() => setSoundAlertsEnabled(!soundAlertsEnabled)}
        title={soundAlertsEnabled ? "Disable sound alerts" : "Enable sound alerts"}
        data-enabled={soundAlertsEnabled}
      >
        {soundAlertsEnabled ? <FaBell /> : <FaBellSlash />}
      </button>
    </div>
  );
};

export default Header;
