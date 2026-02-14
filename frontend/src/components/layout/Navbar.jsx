import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [cartCount, setCartCount] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');

  // Load cart and user data
  useEffect(() => {
    updateCartCount();
    checkAuth();
    
    // Listen for storage changes (cart updates)
    window.addEventListener('storage', updateCartCount);
    return () => window.removeEventListener('storage', updateCartCount);
  }, []);

  // Prevent body scrolling when mobile menu is open
  useEffect(() => {
    if (isMenuOpen) {
      document.body.classList.add('menu-open');
      // Prevent background scrolling on iOS
      document.body.style.overflow = 'hidden';
    } else {
      document.body.classList.remove('menu-open');
      document.body.style.overflow = 'unset';
    }
    
    // Cleanup function
    return () => {
      document.body.classList.remove('menu-open');
      document.body.style.overflow = 'unset';
    };
  }, [isMenuOpen]);

  // Close mobile menu when window is resized to desktop size
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768 && isMenuOpen) {
        setIsMenuOpen(false);
      }
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isMenuOpen]);

  const updateCartCount = () => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    setCartCount(cart.reduce((sum, item) => sum + item.quantity, 0));
  };

  const checkAuth = () => {
    const token = localStorage.getItem('auth_token');
    const email = localStorage.getItem('user_email');
    setIsLoggedIn(!!token);
    if (email) {
      setUserName(email.split('@')[0]);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/shop?search=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
      setIsMenuOpen(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_name');
    setIsLoggedIn(false);
    setIsMenuOpen(false);
    navigate('/');
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo - BIGGER and more prominent */}
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          <img 
            src="/images/logo.jpeg" 
            alt="Lindsay Classics" 
            className="logo-image"
          />
          <span className="logo-text">Lindsay Classics</span>
        </Link>

        {/* Mobile menu button */}
        <button 
          className={`mobile-menu-btn ${isMenuOpen ? 'active' : ''}`}
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle menu"
          aria-expanded={isMenuOpen}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        {/* Navigation Links */}
        <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
          {/* Search Bar - MOVED INSIDE mobile menu for better mobile UX */}
          <form onSubmit={handleSearch} className="search-form mobile-search">
            <input
              type="text"
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit">🔍</button>
          </form>

          <Link to="/" className="nav-link" onClick={closeMenu}>
            Home
          </Link>
          <Link to="/shop" className="nav-link" onClick={closeMenu}>
            Shop
          </Link>
          <Link to="/about" className="nav-link" onClick={closeMenu}>
            About
          </Link>
          <Link to="/contact" className="nav-link" onClick={closeMenu}>
            Contact
          </Link>
        </div>

        {/* Search Bar - Desktop version */}
        <form onSubmit={handleSearch} className="search-form desktop-search">
          <input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit">🔍</button>
        </form>

        {/* User Actions */}
        <div className="navbar-actions">
          <Link to="/cart" className="cart-icon" onClick={closeMenu}>
            🛒
            {cartCount > 0 && <span className="cart-count">{cartCount}</span>}
          </Link>
          
          {isLoggedIn ? (
            <div className="user-menu">
              <button className="user-menu-btn">
                <span className="user-icon">👤</span>
                <span className="user-name">{userName || 'User'}</span>
              </button>
              <div className="user-dropdown">
                <Link to="/profile" onClick={closeMenu}>Profile</Link>
                <Link to="/orders" onClick={closeMenu}>My Orders</Link>
                <button onClick={handleLogout}>Logout</button>
              </div>
            </div>
          ) : (
            <div className="auth-links">
              <Link to="/login" className="auth-link" onClick={closeMenu}>Login</Link>
              <Link to="/register" className="auth-link register" onClick={closeMenu}>Sign Up</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;