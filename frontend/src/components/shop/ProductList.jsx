import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import API from '../../api';
import Navbar from '../layout/Navbar';
import Footer from '../layout/Footer';
import './ProductList.css';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    priceRange: '',
    sort: 'newest',
  });
  const [searchTerm, setSearchTerm] = useState('');
  
  const location = useLocation();
  const navigate = useNavigate();

  // Get category from URL params
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const categoryParam = params.get('category');
    if (categoryParam) {
      setFilters(prev => ({ ...prev, category: categoryParam }));
    }
  }, [location]);

  // Fetch products
  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await API.get('/shop/products/');
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await API.get('/shop/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  // Filter and sort products
  const filteredProducts = products
    .filter(product => {
      // Category filter
      if (filters.category && product.category?.id.toString() !== filters.category) {
        return false;
      }
      
      // Price range filter
      if (filters.priceRange) {
        const [min, max] = filters.priceRange.split('-').map(Number);
        if (max) {
          if (product.price < min || product.price > max) return false;
        } else {
          if (product.price < min) return false;
        }
      }
      
      // Search filter
      if (searchTerm) {
        return product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
               product.description?.toLowerCase().includes(searchTerm.toLowerCase());
      }
      
      return true;
    })
    .sort((a, b) => {
      switch (filters.sort) {
        case 'price-low':
          return a.price - b.price;
        case 'price-high':
          return b.price - a.price;
        case 'name-asc':
          return a.name.localeCompare(b.name);
        case 'name-desc':
          return b.name.localeCompare(a.name);
        default:
          return new Date(b.created_at) - new Date(a.created_at);
      }
    });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    
    // Update URL params
    if (name === 'category') {
      const params = new URLSearchParams(location.search);
      if (value) {
        params.set('category', value);
      } else {
        params.delete('category');
      }
      navigate({ search: params.toString() });
    }
  };

  const clearFilters = () => {
    setFilters({
      category: '',
      priceRange: '',
      sort: 'newest',
    });
    setSearchTerm('');
    navigate('/shop');
  };

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="product-list-page">
      <div className="container">
        {/* Header */}
        <div className="page-header">
          <h1>Our Collection</h1>
          <p className="product-count">{filteredProducts.length} items</p>
        </div>

        {/* Search Bar */}
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <i className="search-icon">🔍</i>
        </div>

        <div className="shop-layout">
          {/* Filters Sidebar */}
          <aside className="filters-sidebar">
            <div className="filters-header">
              <h3>Filters</h3>
              {(filters.category || filters.priceRange || searchTerm) && (
                <button onClick={clearFilters} className="clear-filters">
                  Clear All
                </button>
              )}
            </div>

            {/* Category Filter */}
            <div className="filter-section">
              <h4>Category</h4>
              <select
                name="category"
                value={filters.category}
                onChange={handleFilterChange}
                className="filter-select"
              >
                <option value="">All Categories</option>
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Price Range Filter */}
            <div className="filter-section">
              <h4>Price Range</h4>
              <select
                name="priceRange"
                value={filters.priceRange}
                onChange={handleFilterChange}
                className="filter-select"
              >
                <option value="">All Prices</option>
                <option value="0-1000">Under K1,000</option>
                <option value="1000-5000">K1,000 - K5,000</option>
                <option value="5000-10000">K5,000 - K10,000</option>
                <option value="10000-25000">K10,000 - K25,000</option>
                <option value="25000">Over K25,000</option>
              </select>
            </div>

            {/* Sort Options */}
            <div className="filter-section">
              <h4>Sort By</h4>
              <select
                name="sort"
                value={filters.sort}
                onChange={handleFilterChange}
                className="filter-select"
              >
                <option value="newest">Newest Arrivals</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="name-asc">Name: A to Z</option>
                <option value="name-desc">Name: Z to A</option>
              </select>
            </div>
          </aside>

          {/* Products Grid */}
          <main className="products-grid">
            {filteredProducts.length > 0 ? (
              filteredProducts.map(product => (
                <Link to={`/shop/${product.id}`} key={product.id} className="product-card">
                  <div className="product-image">
                    {product.image && (
                      <img 
                        src={`http://localhost:8000${product.image}`} 
                        alt={product.name}
                        onError={(e) => {
                          e.target.src = '/images/placeholder.jpg';
                        }}
                      />
                    )}
                    {product.compare_at_price && product.compare_at_price > product.price && (
                      <span className="sale-badge">Sale</span>
                    )}
                  </div>
                  <div className="product-details">
                    <h3 className="product-title">{product.name}</h3>
                    <div className="product-pricing">
                      <span className="current-price">K{product.price.toLocaleString()}</span>
                      {product.compare_at_price && product.compare_at_price > product.price && (
                        <span className="original-price">
                          K{product.compare_at_price.toLocaleString()}
                        </span>
                      )}
                    </div>
                    {product.brand && (
                      <span className="product-brand">{product.brand}</span>
                    )}
                  </div>
                </Link>
              ))
            ) : (
              <div className="no-products">
                <h3>No products found</h3>
                <p>Try adjusting your filters or search term</p>
                <button onClick={clearFilters} className="clear-filters-btn">
                  Clear Filters
                </button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );

    return (
    <>
      <Navbar />
      {/* your existing product list content */}
      <Footer />
    </>
  );
};


export default ProductList;