import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            Hyunsoo Han
          </Link>
          <ul className="nav-menu">
            <li className="nav-item">
              <Link to="/" className="nav-link">
                Home
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/cv" className="nav-link">
                CV
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/calendar" className="nav-link">
                Calendar
              </Link>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  );
};

export default Header;