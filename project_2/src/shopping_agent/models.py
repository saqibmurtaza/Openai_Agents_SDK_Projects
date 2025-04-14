# from pydantic import BaseModel
# from typing import List, Optional, Union, Dict, Any

# class Product(BaseModel):
#     """Model representing a product"""
#     product_id: Optional[int] = None
#     name: str
#     category: Optional[str] = None
#     price: float
#     stock: int
#     rating: float
#     description: str
#     image_url: Optional[str] = None

# class SearchResult(BaseModel):
#     """Model representing search results"""
#     products: List[Product]
#     recommended_products: List[Product]
#     message: str
