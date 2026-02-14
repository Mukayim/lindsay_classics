# backend/shop/services/aliexpress.py
from aliexpress_api import AliexpressApi, models
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AliExpressService:
    """Service for interacting with AliExpress API"""
    
    def __init__(self):
        self.client = AliexpressApi(
            settings.ALIEXPRESS_API_KEY,
            settings.ALIEXPRESS_API_SECRET,
            models.Language.EN,
            models.Currency.USD,
            settings.ALIEXPRESS_TRACKING_ID
        )
    
    def search_products(self, keywords, max_price=None, min_price=None, limit=20):
        """Search for products by keywords"""
        try:
            # Prepare search parameters
            params = {
                'keywords': keywords,
                'page_size': limit
            }
            if max_price:
                params['max_sale_price'] = max_price * 100  # API expects cents
            if min_price:
                params['min_sale_price'] = min_price * 100
            
            response = self.client.get_products(**params)
            
            products = []
            for product in response.products:
                products.append({
                    'aliexpress_id': product.product_id,
                    'title': product.product_title,
                    'price': float(product.target_sale_price) / 100,
                    'original_price': float(product.target_original_price) / 100 if product.target_original_price else None,
                    'image_url': product.product_main_image_url,
                    'detail_url': product.product_detail_url,
                    'seller_id': product.seller_id,
                    'seller_name': product.store_name,
                    'orders': product.orders,
                    'rating': product.evaluation_rate,
                    'shipping': self._parse_shipping(product.shipping)
                })
            
            return products
        except Exception as e:
            logger.error(f"AliExpress search failed: {e}")
            return []
    
    def get_product_details(self, product_id):
        """Get detailed information for a specific product"""
        try:
            products = self.client.get_products_details([str(product_id)])
            if products:
                product = products[0]
                return {
                    'aliexpress_id': product.product_id,
                    'title': product.product_title,
                    'description': product.product_description,
                    'price': float(product.target_sale_price) / 100,
                    'images': product.product_image_urls.split(',') if product.product_image_urls else [],
                    'specs': self._parse_specs(product.product_attributes),
                    'seller': {
                        'id': product.seller_id,
                        'name': product.store_name,
                        'rating': product.store_rating
                    }
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get product details: {e}")
            return None
    
    def generate_affiliate_link(self, product_url):
        """Generate affiliate link for tracking"""
        try:
            links = self.client.get_affiliate_links(product_url)
            if links:
                return links[0].promotion_link
            return product_url
        except Exception as e:
            logger.error(f"Failed to generate affiliate link: {e}")
            return product_url
    
    def _parse_shipping(self, shipping_data):
        """Parse shipping information"""
        if not shipping_data:
            return {}
        return {
            'method': shipping_data.get('service_name'),
            'cost': float(shipping_data.get('cost', 0)) / 100 if shipping_data.get('cost') else None,
            'days': shipping_data.get('delivery_time')
        }
    
    def _parse_specs(self, attributes):
        """Parse product attributes into specs"""
        specs = {}
        if attributes:
            for attr in attributes:
                specs[attr.get('name')] = attr.get('value')
        return specs