import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import API from '../../api';
import './ProductDetails.css';

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [relatedProducts, setRelatedProducts] = useState([]);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      const response = await API.get(`/shop/products/${id}/`);
      setProduct(response.data);
      
      // Fetch related products from same category
      if (response.data.category) {
        const relatedRes = await API.get('/shop/products/');
        const related = relatedRes.data
          .filter(p => p.category?.id === response.data.category?.id && p.id !== response.data.id)
          .slice(0, 4);
        setRelatedProducts(related);
      }
    } catch (error) {
      console.error('Error fetching product:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value);
    if (value > 0 && value <= (product?.quantity || 10)) {
      setQuantity(value);
    }
  };

  const handleAddToCart = () => {
    // Get existing cart from localStorage
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    
    // Check if product already in cart
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image,
        quantity: quantity,
      });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Show success message (you can replace with toast notification)
    alert('Product added to cart!');
  };

  const handleBuyNow = () => {
    handleAddToCart();
    navigate('/checkout');
  };

  const images = [
    product?.image,
    product?.image2,
    product?.image3,
  ].filter(Boolean);

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="product-not-found">
        <h2>Product Not Found</h2>
        <p>The product you're looking for doesn't exist.</p>
        <Link to="/shop" className="back-to-shop">Back to Shop</Link>
      </div>
    );
  }

  return (
    <div className="product-details-page">
      <div className="container">
        {/* Breadcrumb */}
        <div className="breadcrumb">
          <Link to="/">Home</Link> / 
          <Link to="/shop">Shop</Link> / 
          {product.category && (
            <>
              <Link to={`/shop?category=${product.category.id}`}>
                {product.category.name}
              </Link> / 
            </>
          )}
          <span>{product.name}</span>
        </div>

        <div className="product-container">
          {/* Product Images */}
          <div className="product-gallery">
            <div className="main-image">
              <img 
                src={images[selectedImage] ? `http://localhost:8000${images[selectedImage]}` : '/images/placeholder.jpg'} 
                alt={product.name}
              />
              {product.compare_at_price && product.compare_at_price > product.price && (
                <span className="sale-badge-large">SALE</span>
              )}
            </div>
            
            {images.length > 1 && (
              <div className="thumbnail-list">
                {images.map((img, index) => (
                  <button
                    key={index}
                    className={`thumbnail ${selectedImage === index ? 'active' : ''}`}
                    onClick={() => setSelectedImage(index)}
                  >
                    <img src={`http://localhost:8000${img}`} alt={`${product.name} - view ${index + 1}`} />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="product-info">
            <h1 className="product-name">{product.name}</h1>
            
            {product.brand && (
              <p className="product-brand">Brand: {product.brand}</p>
            )}
            
            <div className="product-pricing">
              <span className="current-price-large">K{product.price.toLocaleString()}</span>
              {product.compare_at_price && product.compare_at_price > product.price && (
                <>
                  <span className="original-price-large">
                    K{product.compare_at_price.toLocaleString()}
                  </span>
                  <span className="discount-badge">
                    Save K{(product.compare_at_price - product.price).toLocaleString()}
                  </span>
                </>
              )}
            </div>

            <div className="product-availability">
              {product.quantity > 0 ? (
                <span className="in-stock">✓ In Stock ({product.quantity} available)</span>
              ) : (
                <span className="out-of-stock">✗ Out of Stock</span>
              )}
            </div>

            {product.material && (
              <p className="product-material">Material: {product.material}</p>
            )}

            <div className="product-description">
              <h3>Description</h3>
              <p>{product.description}</p>
            </div>

            <div className="product-sku">
              SKU: {product.sku}
            </div>

            {/* Quantity and Actions */}
            <div className="product-actions">
              <div className="quantity-selector">
                <label htmlFor="quantity">Quantity:</label>
                <input
                  type="number"
                  id="quantity"
                  min="1"
                  max={product.quantity || 10}
                  value={quantity}
                  onChange={handleQuantityChange}
                />
              </div>

              <div className="action-buttons">
                <button 
                  className="add-to-cart-btn"
                  onClick={handleAddToCart}
                  disabled={product.quantity === 0}
                >
                  Add to Cart
                </button>
                <button 
                  className="buy-now-btn"
                  onClick={handleBuyNow}
                  disabled={product.quantity === 0}
                >
                  Buy It Now
                </button>
              </div>
            </div>

            {/* Share */}
            <div className="share-section">
              <span>Share this item:</span>
              <div className="share-buttons">
                <button className="share-btn facebook">f</button>
                <button className="share-btn twitter">t</button>
                <button className="share-btn pinterest">p</button>
                <button className="share-btn email">✉</button>
              </div>
            </div>
          </div>
        </div>

        {/* Related Products */}
        {relatedProducts.length > 0 && (
          <div className="related-products">
            <h2>You May Also Like</h2>
            <div className="related-grid">
              {relatedProducts.map(related => (
                <Link to={`/shop/${related.id}`} key={related.id} className="related-card">
                  <div className="related-image">
                    <img 
                      src={related.image ? `http://localhost:8000${related.image}` : '/images/placeholder.jpg'} 
                      alt={related.name}
                    />
                  </div>
                  <div className="related-info">
                    <h3>{related.name}</h3>
                    <p className="related-price">K{related.price.toLocaleString()}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductDetails;