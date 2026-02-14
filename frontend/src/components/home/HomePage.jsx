import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../layout/Navbar';
import Footer from '../layout/Footer';
import './HomePage.css';

const HomePage = () => {
  // Featured categories
  const categories = [
    { id: 1, name: 'Classic Watches', image: '/images/categories/watches.jpg', count: 24 },
    { id: 2, name: 'Vintage Jewelry', image: '/images/categories/jewelry.jpg', count: 18 },
    { id: 3, name: 'Antique Furniture', image: '/images/categories/furniture.jpg', count: 12 },
    { id: 4, name: 'Rare Books', image: '/images/categories/books.jpg', count: 45 },
  ];

  // Featured products (you'll replace with API data later)
  const featuredProducts = [
    { id: 1, name: 'Rolex Submariner 1960s', price: 12500, image: '/images/products/watch1.jpg' },
    { id: 2, name: 'Victorian Diamond Brooch', price: 3450, image: '/images/products/brooch1.jpg' },
    { id: 3, name: 'Louis XVI Writing Desk', price: 8900, image: '/images/products/desk1.jpg' },
    { id: 4, name: 'First Edition Hemingway', price: 1250, image: '/images/products/book1.jpg' },
  ];

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Discover Timeless Elegance</h1>
          <p>Curated collection of the finest classic pieces from around the world</p>
          <Link to="/shop" className="cta-button">Explore Collection</Link>
        </div>
      </section>

      {/* Categories Section */}
      <section className="categories">
        <div className="container">
          <h2 className="section-title">Shop by Category</h2>
          <div className="category-grid">
            {categories.map(category => (
              <Link to={`/shop?category=${category.id}`} key={category.id} className="category-card">
                <div className="category-image" style={{ backgroundImage: `url(${category.image})` }}>
                  <div className="category-overlay">
                    <h3>{category.name}</h3>
                    <p>{category.count} items</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="featured">
        <div className="container">
          <h2 className="section-title">Featured Pieces</h2>
          <div className="product-grid">
            {featuredProducts.map(product => (
              <Link to={`/shop/${product.id}`} key={product.id} className="product-card">
                <div className="product-image">
                  <img src={product.image} alt={product.name} />
                </div>
                <div className="product-info">
                  <h3>{product.name}</h3>
                  <p className="product-price">K{product.price.toLocaleString()}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="newsletter">
        <div className="container">
          <div className="newsletter-content">
            <h2>Join Our Collector's Circle</h2>
            <p>Subscribe to receive exclusive offers and early access to new arrivals</p>
            <form className="newsletter-form">
              <input type="email" placeholder="Your email address" />
              <button type="submit">Subscribe</button>
            </form>
          </div>
        </div>
      </section>

      {/* Brand Story */}
      <section className="story">
        <div className="container">
          <div className="story-content">
            <h2>The Lindsay Classics Story</h2>
            <p>
              For over three decades, Lindsay Classics has been the premier destination 
              for discerning collectors seeking the finest classic and vintage pieces. 
              Each item in our collection is carefully authenticated and restored to 
              preserve its historical significance and beauty.
            </p>
            <Link to="/about" className="story-link">Learn More About Us →</Link>
          </div>
        </div>
      </section>
    </div>
  );
  
  return (
    <>
      <Navbar />
      {/* Your existing HomePage content */}
      <div className="homepage">
        {/* ... all your existing homepage sections ... */}
      </div>
      <Footer />
    </>
  );
};

export default HomePage;