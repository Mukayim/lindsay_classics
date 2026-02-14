import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Cart.css';

const Cart = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [couponCode, setCouponCode] = useState('');
  const [discount, setDiscount] = useState(0);

  // Load cart from localStorage
  useEffect(() => {
    loadCart();
  }, []);

  const loadCart = () => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setCartItems(JSON.parse(savedCart));
    }
  };

  // Save cart to localStorage
  const saveCart = (items) => {
    localStorage.setItem('cart', JSON.stringify(items));
    setCartItems(items);
  };

  // Update quantity
  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) return;
    
    const updatedCart = cartItems.map(item =>
      item.id === productId ? { ...item, quantity: newQuantity } : item
    );
    saveCart(updatedCart);
  };

  // Remove item from cart
  const removeItem = (productId) => {
    const updatedCart = cartItems.filter(item => item.id !== productId);
    saveCart(updatedCart);
  };

  // Clear entire cart
  const clearCart = () => {
    if (window.confirm('Are you sure you want to clear your cart?')) {
      localStorage.removeItem('cart');
      setCartItems([]);
    }
  };

  // Calculate subtotal
  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  // Calculate shipping (free over K1000)
  const shipping = subtotal > 1000 ? 0 : 50;

  // Calculate tax (16% VAT)
  const tax = subtotal * 0.16;

  // Calculate total
  const total = subtotal + shipping + tax - discount;

  // Apply coupon
  const applyCoupon = () => {
    if (couponCode.toUpperCase() === 'WELCOME10') {
      setDiscount(subtotal * 0.1);
      alert('Coupon applied! 10% discount');
    } else if (couponCode.toUpperCase() === 'FREESHIP') {
      setDiscount(shipping);
      alert('Free shipping applied!');
    } else {
      alert('Invalid coupon code');
    }
    setCouponCode('');
  };

  // Proceed to checkout
  const proceedToCheckout = () => {
    if (cartItems.length === 0) {
      alert('Your cart is empty');
      return;
    }
    navigate('/checkout');
  };

  if (cartItems.length === 0) {
    return (
      <div className="empty-cart">
        <div className="empty-cart-content">
          <span className="empty-cart-icon">🛒</span>
          <h2>Your Cart is Empty</h2>
          <p>Looks like you haven't added anything to your cart yet.</p>
          <Link to="/shop" className="continue-shopping-btn">
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <div className="container">
        <h1 className="cart-title">Shopping Cart</h1>
        
        <div className="cart-layout">
          {/* Cart Items */}
          <div className="cart-items">
            {cartItems.map(item => (
              <div key={item.id} className="cart-item">
                <div className="item-image">
                  <img 
                    src={item.image ? `http://localhost:8000${item.image}` : '/images/placeholder.jpg'} 
                    alt={item.name}
                  />
                </div>
                
                <div className="item-details">
                  <h3 className="item-name">{item.name}</h3>
                  <p className="item-price">K{item.price.toLocaleString()}</p>
                </div>
                
                <div className="item-quantity">
                  <button 
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    className="quantity-btn"
                  >
                    -
                  </button>
                  <span className="quantity-value">{item.quantity}</span>
                  <button 
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="quantity-btn"
                  >
                    +
                  </button>
                </div>
                
                <div className="item-total">
                  K{(item.price * item.quantity).toLocaleString()}
                </div>
                
                <button 
                  onClick={() => removeItem(item.id)}
                  className="remove-item"
                  title="Remove item"
                >
                  ×
                </button>
              </div>
            ))}
            
            <div className="cart-actions">
              <button onClick={clearCart} className="clear-cart-btn">
                Clear Cart
              </button>
              <Link to="/shop" className="continue-shopping-link">
                Continue Shopping
              </Link>
            </div>
          </div>

          {/* Cart Summary */}
          <div className="cart-summary">
            <h2>Order Summary</h2>
            
            <div className="summary-row">
              <span>Subtotal</span>
              <span>K{subtotal.toFixed(2)}</span>
            </div>
            
            <div className="summary-row">
              <span>Shipping</span>
              <span>{shipping === 0 ? 'Free' : `K${shipping.toFixed(2)}`}</span>
            </div>
            
            <div className="summary-row">
              <span>Tax (16% VAT)</span>
              <span>K{tax.toFixed(2)}</span>
            </div>
            
            {discount > 0 && (
              <div className="summary-row discount">
                <span>Discount</span>
                <span>-K{discount.toFixed(2)}</span>
              </div>
            )}
            
            <div className="summary-row total">
              <span>Total</span>
              <span>K{total.toFixed(2)}</span>
            </div>

            {/* Coupon Code */}
            <div className="coupon-section">
              <input
                type="text"
                placeholder="Coupon code"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value)}
              />
              <button onClick={applyCoupon}>Apply</button>
            </div>
            
            <button 
              onClick={proceedToCheckout}
              className="checkout-btn"
            >
              Proceed to Checkout
            </button>
            
            <div className="payment-icons">
              <span>💳</span>
              <span>📱</span>
              <span>💵</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;