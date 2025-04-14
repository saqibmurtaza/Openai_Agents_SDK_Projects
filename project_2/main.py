# from shopping_agent.shopping_agents import shopping_manager
# from shopping_agent.config_agents import config
# from agents import Runner
# import chainlit as cl
# import re
# import json
# import asyncio

# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("stage", "awaiting_query")
#     cl.user_session.set("cart", [])
#     await cl.Message(content="👋 Hi! What product are you looking for?").send()

# @cl.on_message
# async def handle_message(message: cl.Message):
#     stage = cl.user_session.get("stage")
#     cart = cl.user_session.get("cart", [])
    
#     # Handle different user intents based on message content
#     user_input = message.content.strip().lower()
    
#     # Handle refine search
#     if user_input.startswith("refine "):
#         query = user_input[7:].strip()  # Extract the query after "refine "
#         if not query:
#             await cl.Message(content="Please provide a search term after 'refine'.").send()
#             return
            
#         # Execute search with the refined query
#         async with cl.Step(name="Searching products..."):
#             run_result = await Runner.run(
#                 shopping_manager,
#                 query,
#                 run_config=config
#             )
#             # Extract the response string from the RunResult object
#             response = run_result.final_output
#             print(f"Raw response from refine search: {response}")
        
#         try:
#             # Extract JSON from markdown code block if present
#             json_data = extract_json_from_response(response)
#             print(f"Extracted JSON data: {json_data}")
            
#             products = json_data.get("products", [])
#             recommended = json_data.get("recommended_products", [])
            
#             print(f"Found {len(products)} products and {len(recommended)} recommended items")
            
#             if not products:
#                 await cl.Message(content="No products found matching your refined search.").send()
#             else:
#                 # Display search results
#                 products_text = "Here are the products matching your search:\n\n"
#                 for i, product in enumerate(products, 1):
#                     products_text += f"{i}. **{product['name']}** - ${product['price']}\n"
#                     products_text += f"   Rating: {product['rating']} | Stock: {product['stock']}\n"
#                     products_text += f"   Description: {product['description']}\n\n"
                
#                 if recommended:
#                     products_text += "You might also be interested in:\n\n"
#                     for i, product in enumerate(recommended, 1):
#                         products_text += f"• **{product['name']}** - ${product['price']}\n"
                
#                 await cl.Message(content=products_text).send()
                
#                 # Store the search results for later use
#                 cl.user_session.set("last_search_results", products)
#                 cl.user_session.set("last_recommended", recommended)
#         except Exception as e:
#             print(f"Error parsing response: {e}")
#             print(f"Response type: {type(response)}")
#             print(f"Response content: {response}")
#             await cl.Message(content="Sorry, there was an error processing your search.").send()
    
#     # Handle add to cart
#     elif user_input.startswith("add "):
#         product_name = user_input[4:].strip()  # Extract the product name after "add "
        
#         if not product_name:
#             await cl.Message(content="Please specify which product you want to add to your cart.").send()
#             return
            
#         # Check if we have search results to add from
#         last_search_results = cl.user_session.get("last_search_results", [])
#         last_recommended = cl.user_session.get("last_recommended", [])
#         all_products = last_search_results + last_recommended
        
#         # Find the product in the search results
#         found_product = None
#         for product in all_products:
#             if product_name.lower() in product['name'].lower():
#                 found_product = product
#                 break
        
#         if found_product:
#             # Add to cart
#             cart.append(found_product)
#             cl.user_session.set("cart", cart)
            
#             await cl.Message(content=f"Added **{found_product['name']}** to your cart. You now have {len(cart)} item(s) in your cart.").send()
#         else:
#             await cl.Message(content=f"Sorry, I couldn't find '{product_name}' in the search results. Please search for the product first.").send()
    
#     # Handle view cart
#     elif user_input == "view cart":
#         if not cart:
#             await cl.Message(content="Your cart is empty.").send()
#         else:
#             cart_text = "Your cart contains:\n\n"
#             total = 0
#             for i, item in enumerate(cart, 1):
#                 cart_text += f"{i}. **{item['name']}** - ${item['price']}\n"
#                 total += item['price']
            
#             cart_text += f"\n**Total: ${total}**"
#             await cl.Message(content=cart_text).send()
    
#     # Handle checkout
#     elif user_input == "checkout":
#         if not cart:
#             await cl.Message(content="Your cart is empty. Please add items before checking out.").send()
#         else:
#             # Calculate total
#             total = sum(item['price'] for item in cart)
            
#             # Display checkout summary
#             checkout_text = "**Checkout Summary**\n\n"
#             for i, item in enumerate(cart, 1):
#                 checkout_text += f"{i}. {item['name']} - ${item['price']}\n"
            
#             checkout_text += f"\n**Total: ${total}**\n\n"
#             checkout_text += "Thank you for your purchase! Your order has been placed."
            
#             await cl.Message(content=checkout_text).send()
            
#             # Reset cart after checkout
#             cl.user_session.set("cart", [])
    
#     # Handle initial product search
#     elif stage == "awaiting_query":
#         query = user_input
        
#         # Show typing indicator
#         async with cl.Step(name="Searching products..."):
#             run_result = await Runner.run(
#                 shopping_manager,
#                 query,
#                 run_config=config
#             )
#             # Extract the response string from the RunResult object
#             response = run_result.final_output
#             print(f"Raw response from initial search: {response}")
        
#         try:
#             # Extract JSON from markdown code block if present
#             json_data = extract_json_from_response(response)
#             print(f"Extracted JSON data: {json_data}")
            
#             products = json_data.get("products", [])
#             recommended = json_data.get("recommended_products", [])
            
#             print(f"Found {len(products)} products and {len(recommended)} recommended items")
            
#             if not products:
#                 await cl.Message(content="Sorry, I couldn't find any products matching your search.").send()
#             else:
#                 # Display search results
#                 products_text = "Here are the products matching your search:\n\n"
#                 for i, product in enumerate(products, 1):
#                     products_text += f"{i}. **{product['name']}** - ${product['price']}\n"
#                     products_text += f"   Rating: {product['rating']} | Stock: {product['stock']}\n"
#                     products_text += f"   Description: {product['description']}\n\n"
                
#                 if recommended:
#                     products_text += "You might also be interested in:\n\n"
#                     for i, product in enumerate(recommended, 1):
#                         products_text += f"• **{product['name']}** - ${product['price']}\n"
                
#                 await cl.Message(content=products_text).send()
                
#                 # Store the search results for later use
#                 cl.user_session.set("last_search_results", products)
#                 cl.user_session.set("last_recommended", recommended)
#         except Exception as e:
#             print(f"Error parsing response: {e}")
#             print(f"Response type: {type(response)}")
#             print(f"Response content: {response}")
#             await cl.Message(content="Sorry, there was an error processing your search.").send()
    
#     # Display follow-up options after every interaction
#     follow_up_text = (
#         "\n\nWhat would you like to do next?\n"
#         "Type 'refine <query>' to refine your search,\n"
#         "or 'add <product name>' to add another item to your cart,\n"
#         "or 'view cart' to see your cart,\n"
#         "or 'checkout' to proceed to checkout."
#     )
    
#     await cl.Message(content=follow_up_text).send()

# def extract_json_from_response(response):
#     """
#     Extract JSON data from a response that might be wrapped in a markdown code block.
#     """
#     if isinstance(response, dict):
#         return response
    
#     # Check if the response is a string with a markdown code block
#     if isinstance(response, str):
#         # Try to extract JSON from markdown code block
#         json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
#         if json_match:
#             json_str = json_match.group(1)
#             try:
#                 return json.loads(json_str)
#             except json.JSONDecodeError as e:
#                 print(f"Error parsing JSON from code block: {e}")
#                 print(f"Extracted string: {json_str}")
        
#         # If no code block, try to parse the entire string as JSON
#         try:
#             return json.loads(response)
#         except json.JSONDecodeError:
#             # If that fails, look for a JSON-like structure in the string
#             json_start = response.find('{')
#             json_end = response.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 json_str = response[json_start:json_end]
#                 try:
#                     return json.loads(json_str)
#                 except json.JSONDecodeError as e:
#                     print(f"Error parsing JSON substring: {e}")
#                     print(f"Extracted substring: {json_str}")
        
#         # Try to extract from the SearchTool output in the log
#         search_tool_match = re.search(r'SearchTool:\s*(\{.*\})', response, re.DOTALL)
#         if search_tool_match:
#             json_str = search_tool_match.group(1)
#             try:
#                 return json.loads(json_str)
#             except json.JSONDecodeError as e:
#                 print(f"Error parsing SearchTool JSON: {e}")
#                 print(f"Extracted SearchTool string: {json_str}")
    
#     # If all else fails, return an empty dict
#     print("Could not extract JSON from response, returning empty dict")
#     return {}


from shopping_agent.shopping_agents import shopping_manager
from shopping_agent.config_agents import config
from agents import Runner
import chainlit as cl
import asyncio
import json
import re

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("stage", "awaiting_query")
    cl.user_session.set("cart", [])
    await cl.Message(content="👋 Hi! What product are you looking for?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    stage = cl.user_session.get("stage")
    cart = cl.user_session.get("cart", [])
    
    # Handle different user intents based on message content
    user_input = message.content.strip().lower()
    
    # Handle refine search
    if user_input.startswith("refine "):
        query = user_input[7:].strip()  # Extract the query after "refine "
        if not query:
            await cl.Message(content="Please provide a search term after 'refine'.").send()
            return
            
        # Execute search with the refined query
        async with cl.Step(name="Searching products..."):
            run_result = await Runner.run(
                shopping_manager,
                query,
                run_config=config
            )
            # Extract the response string from the RunResult object
            response = run_result.final_output
            print(f"Raw response from refine search: {response}")
        
        try:
            # Extract structured data from the response
            search_result = extract_search_result(response)
            print(f"Extracted search result: {search_result}")
            
            products = search_result.get("products", [])
            recommended = search_result.get("recommended_products", [])
            
            if not products:
                # If no structured data found, check if the response is a readable message
                if isinstance(response, str) and len(response) > 0:
                    await cl.Message(content=response).send()
                else:
                    await cl.Message(content="No products found matching your refined search.").send()
            else:
                # Display search results
                products_text = "Here are the products matching your search:\n\n"
                for i, product in enumerate(products, 1):
                    products_text += f"{i}. **{product['name']}** - ${product['price']}\n"
                    products_text += f"   Rating: {product['rating']} | Stock: {product['stock']}\n"
                    products_text += f"   Description: {product['description']}\n\n"
                
                if recommended:
                    products_text += "You might also be interested in:\n\n"
                    for i, product in enumerate(recommended, 1):
                        products_text += f"• **{product['name']}** - ${product['price']}\n"
                
                await cl.Message(content=products_text).send()
                
                # Store the search results for later use
                cl.user_session.set("last_search_results", products)
                cl.user_session.set("last_recommended", recommended)
        except Exception as e:
            print(f"Error processing search result: {e}")
            print(f"Result type: {type(response)}")
            print(f"Result content: {response}")
            
            # If we encounter an error but have a readable response, display it
            if isinstance(response, str) and len(response) > 0:
                await cl.Message(content=response).send()
            else:
                await cl.Message(content="Sorry, there was an error processing your search.").send()
    
    # Handle add to cart
    elif user_input.startswith("add "):
        product_name = user_input[4:].strip()  # Extract the product name after "add "
        
        if not product_name:
            await cl.Message(content="Please specify which product you want to add to your cart.").send()
            return
            
        # Check if we have search results to add from
        last_search_results = cl.user_session.get("last_search_results", [])
        last_recommended = cl.user_session.get("last_recommended", [])
        all_products = last_search_results + last_recommended
        
        # Find the product in the search results
        found_product = None
        for product in all_products:
            if product_name.lower() in product['name'].lower():
                found_product = product
                break
        
        if found_product:
            # Add to cart
            cart.append(found_product)
            cl.user_session.set("cart", cart)
            
            await cl.Message(content=f"Added **{found_product['name']}** to your cart. You now have {len(cart)} item(s) in your cart.").send()
        else:
            await cl.Message(content=f"Sorry, I couldn't find '{product_name}' in the search results. Please search for the product first.").send()
    
    # Handle view cart
    elif user_input == "view cart":
        if not cart:
            await cl.Message(content="Your cart is empty.").send()
        else:
            cart_text = "Your cart contains:\n\n"
            total = 0
            for i, item in enumerate(cart, 1):
                cart_text += f"{i}. **{item['name']}** - ${item['price']}\n"
                total += item['price']
            
            cart_text += f"\n**Total: ${total}**"
            await cl.Message(content=cart_text).send()
    
    # Handle checkout
    elif user_input == "checkout":
        if not cart:
            await cl.Message(content="Your cart is empty. Please add items before checking out.").send()
        else:
            # Calculate total
            total = sum(item['price'] for item in cart)
            
            # Display checkout summary
            checkout_text = "**Checkout Summary**\n\n"
            for i, item in enumerate(cart, 1):
                checkout_text += f"{i}. {item['name']} - ${item['price']}\n"
            
            checkout_text += f"\n**Total: ${total}**\n\n"
            checkout_text += "Thank you for your purchase! Your order has been placed."
            
            await cl.Message(content=checkout_text).send()
            
            # Reset cart after checkout
            cl.user_session.set("cart", [])
    
    # Handle initial product search
    elif stage == "awaiting_query":
        query = user_input
        
        # Show typing indicator
        async with cl.Step(name="Searching products..."):
            run_result = await Runner.run(
                shopping_manager,
                query,
                run_config=config
            )
            # Extract the response string from the RunResult object
            response = run_result.final_output
            print(f"Raw response from initial search: {response}")
        
        try:
            # Extract structured data from the response
            search_result = extract_search_result(response)
            print(f"Extracted search result: {search_result}")
            
            products = search_result.get("products", [])
            recommended = search_result.get("recommended_products", [])
            
            if not products:
                # If no structured data found, check if the response is a readable message
                if isinstance(response, str) and len(response) > 0:
                    await cl.Message(content=response).send()
                else:
                    await cl.Message(content="Sorry, I couldn't find any products matching your search.").send()
            else:
                # Display search results
                products_text = "Here are the products matching your search:\n\n"
                for i, product in enumerate(products, 1):
                    products_text += f"{i}. **{product['name']}** - ${product['price']}\n"
                    products_text += f"   Rating: {product['rating']} | Stock: {product['stock']}\n"
                    products_text += f"   Description: {product['description']}\n\n"
                
                if recommended:
                    products_text += "You might also be interested in:\n\n"
                    for i, product in enumerate(recommended, 1):
                        products_text += f"• **{product['name']}** - ${product['price']}\n"
                
                await cl.Message(content=products_text).send()
                
                # Store the search results for later use
                cl.user_session.set("last_search_results", products)
                cl.user_session.set("last_recommended", recommended)
        except Exception as e:
            print(f"Error processing search result: {e}")
            print(f"Result type: {type(response)}")
            print(f"Result content: {response}")
            
            # If we encounter an error but have a readable response, display it
            if isinstance(response, str) and len(response) > 0:
                await cl.Message(content=response).send()
            else:
                await cl.Message(content="Sorry, there was an error processing your search.").send()
    
    # Display follow-up options after every interaction
    follow_up_text = (
        "\n\nWhat would you like to do next?\n"
        "Type 'refine <query>' to refine your search,\n"
        "or 'add <product name>' to add another item to your cart,\n"
        "or 'view cart' to see your cart,\n"
        "or 'checkout' to proceed to checkout."
    )
    
    await cl.Message(content=follow_up_text).send()

def extract_search_result(response):
    """
    Extract structured search result from various response formats.
    Returns a dictionary with products and recommended_products.
    """
    # If response is already a dictionary, return it
    if isinstance(response, dict):
        return response
    
    # If response is a string, try to extract JSON
    if isinstance(response, str):
        # Try to extract JSON from markdown code block
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try to parse the entire string as JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON-like structure in the string
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try to extract from SearchTool output
        search_tool_match = re.search(r'SearchTool:\s*(\{.*\})', response, re.DOTALL)
        if search_tool_match:
            json_str = search_tool_match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # If all JSON extraction fails, try to parse human-readable format
        return extract_products_from_text(response)
    
    # If all else fails, return empty result
    return {"products": [], "recommended_products": []}

def extract_products_from_text(text):
    """
    Extract product information from a text response.
    Returns a dictionary with products and recommended_products.
    """
    products = []
    recommended_products = []
    
    # Check if this is a human-readable product list
    if "**" in text and "$" in text:
        # Split the text into main products and recommended products
        main_section = text
        recommended_section = ""
        
        if "also" in text.lower() and "interested in" in text.lower():
            parts = re.split(r'(?i)we also have|you might also be interested in|also recommended', text)
            if len(parts) > 1:
                main_section = parts[0]
                recommended_section = parts[1]
        
        # Extract main products
        product_matches = re.finditer(r'\*\*([^*]+)\*\*:?\s*\$(\d+),?\s*(\d+) in stock,?\s*(\d+\.?\d*) rating\.?\s*([^*\n]+)', main_section)
        for match in product_matches:
            name = match.group(1).strip()
            price = int(match.group(2))
            stock = int(match.group(3))
            rating = float(match.group(4))
            description = match.group(5).strip()
            
            products.append({
                'name': name,
                'price': price,
                'stock': stock,
                'rating': rating,
                'description': description
            })
        
        # Extract recommended products
        if recommended_section:
            rec_matches = re.finditer(r'\*\*([^*]+)\*\*:?\s*\$(\d+),?\s*(\d+) in stock,?\s*(\d+\.?\d*) rating\.?\s*([^*\n]+)', recommended_section)
            for match in rec_matches:
                name = match.group(1).strip()
                price = int(match.group(2))
                stock = int(match.group(3))
                rating = float(match.group(4))
                description = match.group(5).strip()
                
                recommended_products.append({
                    'name': name,
                    'price': price,
                    'stock': stock,
                    'rating': rating,
                    'description': description
                })
    
    return {"products": products, "recommended_products": recommended_products}
