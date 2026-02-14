# backend/shop/services/aliexpress_client.py
import requests
import hashlib
import time
import hmac
from urllib.parse import urlencode
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AliExpressClient:
    """Custom AliExpress API client"""
    
    def __init__(self):
        self.app_key = settings.ALIEXPRESS_API_KEY
        self.app_secret = settings.ALIEXPRESS_API_SECRET
        self.tracking_id = settings.ALIEXPRESS_TRACKING_ID
        self.base_url = "https://api.aliexpress.com/rest"
        self.format = "json"
        self.sign_method = "sha256"
    
    def _generate_signature(self, params):
        """Generate API signature"""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())
        
        # Create string to sign
        string_to_sign = self.app_secret
        for key, value in sorted_params:
            string_to_sign += key + value
        string_to_sign += self.app_secret
        
        # Generate signature
        signature = hashlib.sha256(string_to_sign.encode('utf-8')).hexdigest().upper()
        return signature
    
    def _request(self, method, params):
        """Make API request"""
        # Add common parameters
        params.update({
            'app_key': self.app_key,
            'format': self.format,
            'sign_method': self.sign_method,
            'timestamp': str(int(time.time() * 1000)),
            'v': '2.0',
        })
        
        # Generate signature
        params['sign'] = self._generate_signature(params)
        
        # Make request
        url = f"{self.base_url}/{method}"
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API request failed: {response.status_code}")
            return None
    
    def search_products(self, keywords, max_price=None, min_price=None, limit=20):
        """Search for products by keywords"""
        try:
            products = self.client.search_products(
                keywords=keywords,
                min_price=min_price,
                max_price=max_price,
                page_size=limit
            )
            
            results = []
            for product in products:
                results.append({
                    'aliexpress_id': product.get('product_id'),
                    'title': product.get('product_title'),
                    'price': float(product.get('sale_price', 0)) / 100,
                    'original_price': float(product.get('original_price', 0)) / 100 if product.get('original_price') else None,
                    'image_url': product.get('product_main_image_url'),
                    'detail_url': product.get('product_detail_url'),
                    'seller_id': product.get('seller_id'),
                    'seller_name': product.get('store_name'),
                    'orders': product.get('orders', 0),
                    'rating': product.get('evaluate_rate'),
                    'shipping': {
                        'cost': float(product.get('shipping_cost', 0)) / 100,
                        'days': product.get('shipping_days'),
                        'method': product.get('shipping_method')
                    }
                })
            
            return results
        except Exception as e:
            logger.error(f"AliExpress search failed: {e}")
            return []
    
    def get_product_details(self, product_ids):
        """Get product details"""
        if isinstance(product_ids, list):
            product_ids = ','.join(str(id) for id in product_ids)
        
        params = {
            'method': 'aliexpress.affiliate.product.detail.get',
            'product_ids': product_ids,
            'tracking_id': self.tracking_id,
        }
        
        response = self._request('api', params)
        
        if response and 'aliexpress_affiliate_product_detail_get_response' in response:
            data = response['aliexpress_affiliate_product_detail_get_response']
            if 'products' in data:
                return data['products'].get('product', [])
        
        return []
    
    def get_affiliate_links(self, product_urls):
        """Generate affiliate links"""
        if isinstance(product_urls, list):
            product_urls = ','.join(product_urls)
        
        params = {
            'method': 'aliexpress.affiliate.link.generate',
            'source_values': product_urls,
            'tracking_id': self.tracking_id,
        }
        
        response = self._request('api', params)
        
        if response and 'aliexpress_affiliate_link_generate_response' in response:
            data = response['aliexpress_affiliate_link_generate_response']
            if 'promotion_links' in data:
                return data['promotion_links'].get('promotion_link', [])
        
        return []