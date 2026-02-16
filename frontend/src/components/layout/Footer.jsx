import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        
        <div className="footer-section">
          <div className="footer-logo">
            <img src="/static/vite/images/logo.jpeg" alt="Lindsay Classics" />
            <h3>Lindsay Classics</h3>
          </div>
          <p>Your premier destination for classic luxury items since 1990.</p>
          <div className="social-links">
            <a href="#" className="social-link">📘</a>
            <a href="#" className="social-link">📷</a>
            <a href="#" className="social-link">🐦</a>
            <a href="#" className="social-link">📌</a>
          </div>
        </div>

        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/shop">Shop</Link></li>
            <li><Link to="/about">About Us</Link></li>
            <li><Link to="/contact">Contact</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Customer Service</h4>
          <ul>
            <li><Link to="/faq">FAQ</Link></li>
            <li><Link to="/shipping">Shipping Info</Link></li>
            <li><Link to="/returns">Returns</Link></li>
            <li><Link to="/privacy">Privacy Policy</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Contact Info</h4>
          <ul className="contact-info">
            <li>📍 Lusaka, Zambia</li>
            <li>📞 +260 123 456 789</li>
            <li>✉️ info@lindsayclassics.com</li>
            <li>🕒 Mon-Fri: 9am - 6pm</li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; 2026 Lindsay Classics. All rights reserved.</p>
        <div className="payment-icons">
          <span>💳</span>
          <span>📱</span>
          <span>💵</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
