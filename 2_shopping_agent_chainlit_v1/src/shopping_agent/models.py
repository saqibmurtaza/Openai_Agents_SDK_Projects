###########################################
"""
when using pydantic, gemini-1.5-flash with openai-agents-sdk,
it  generate error like:
openai.BadRequestError: Error code: 400 - [{'error': {'code': 400, 'message': 'Request contains an invalid argument.', 'status': 'INVALID_ARGUMENT'}}]
The error message s being raised by OpenAI's Python SDK because you're 
running the Agents SDK built on OpenAI's tools — but behind the scenes 
you're using Gemini as your LLM via OpenAIChatCompletionsModel 
(configured with gemini/gemini-1.5-flash).
This is a tool-call serialization issue. Gemini is rejecting the tool's schema or 
the function output you're returning.
ISSUE NOT RESLOVED; therefore, using alternate approach:

- remove output_type from Agent
- schema defined in Agents instructions
"""


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
