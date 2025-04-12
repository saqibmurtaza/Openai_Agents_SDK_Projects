from shopping_agent.shopping_agents import shopping_manager
from shopping_agent.config_agents import config
from agents import Runner
import chainlit as cl, re, json, asyncio

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("stage", "awaiting_query")
    cl.user_session.set("cart", [])
    await cl.Message(content="👋 Hi! What product are you looking for?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    stage = cl.user_session.get("stage")
    user_input = message.content.strip()

    if user_input.lower().startswith("refine "):
        refined_query = user_input[7:]
        cl.user_session.set("query", refined_query)
        await run_product_search(refined_query)

    elif user_input.lower().startswith("add "):
        product_name = user_input[4:].strip().lower()
        products = cl.user_session.get("products") or []
        selected = next((p for p in products if p["name"].lower() == product_name), None)
        if selected:
            cart = cl.user_session.get("cart")
            cart.append(selected)
            cl.user_session.set("cart", cart)
            await cl.Message(content=f"✅ Added **{selected['name']}** to your cart.").send()
        else:
            await cl.Message(content="⚠️ Couldn't find that product in the current results.").send()

    elif user_input.lower() == "view cart":
        cart = cl.user_session.get("cart")
        if not cart:
            await cl.Message(content="🛒 Your cart is empty.").send()
        else:
            formatted = [f"- **{item['name']}** (${item['price']})" for item in cart]
            await cl.Message(content="🛒 **Your Cart:**\n" + "\n".join(formatted)).send()

    elif user_input.lower() == "checkout":
        cart = cl.user_session.get("cart")
        if not cart:
            await cl.Message(content="🛒 Your cart is empty.").send()
        else:
            total = sum(item["price"] for item in cart)
            formatted = [f"- {item['name']} (${item['price']})" for item in cart]
            receipt = "\n".join(formatted)
            await cl.Message(content=f"✅ **Checkout Summary**\n{receipt}\n\nTotal: ${total}").send()
            cl.user_session.set("cart", [])

    elif stage == "awaiting_query":
        cl.user_session.set("query", user_input)
        await run_product_search(user_input)

async def get_recommendation_reason(product: dict) -> str:
    """
    Uses the LLM to generate a recommendation reason for a given product.
    The prompt passes product details to obtain a natural recommendation explanation.
    """
    prompt = (
        f"Product details:\n"
        f"Name: {product['name']}\n"
        f"Price: ${product['price']}\n"
        f"Stock: {product.get('stock', 'N/A')}\n"
        f"Category: {product['category']}\n"
        f"Description: {product.get('description', 'No description available')}\n\n"
        "Please provide a single sentence explanation (without apologies or error messages) "
        "describing why this product is recommended to a customer."
    )
    res = await Runner.run(
        shopping_manager, 
        prompt, 
        run_config=config)
    return res.final_output.strip()

async def run_product_search(query):
    result = await Runner.run(
        shopping_manager,
        query,
        run_config=config
    )

    final_output = result.final_output
    # Extract the JSON object from the output using regex.
    match = re.search(r'({.*})', final_output, re.DOTALL)
    if not match:
        await cl.Message(content="❌ Invalid response format from search").send()
        return

    json_str = match.group(1).strip()
    output_data = json.loads(json_str)

    products = output_data.get("products", [])
    recommended = output_data.get("recommended_products", [])
    cl.user_session.set("products", products)

    if not products:
        await cl.Message(content="❌ No matching products found.").send()
    else:
        # Format primary products with full details.
        formatted_products = [
            (
                f"**{i+1}. {p['name']}**\n"
                f"💰 Price: ${p['price']}  |  "
                f"📦 Stock: {p.get('stock', 'N/A')}  |  "
                f"🏷️ Category: {p['category']}\n"
                f"{p.get('description', 'No description available')}"
            )
            for i, p in enumerate(products)
        ]
        response = "\n\n".join(formatted_products)

        # For recommended products, get a dynamic recommendation reason from the LLM.
        if recommended:
            reasons = await asyncio.gather(*(get_recommendation_reason(p) for p in recommended))
            formatted_recommended = [
                (
                    f"**{i+1}. {p['name']}**\n"
                    f"💰 Price: ${p['price']}  |  "
                    f"📦 Stock: {p.get('stock', 'N/A')}  |  "
                    f"🏷️ Category: {p['category']}\n"
                    f"{p.get('description', 'No description available')}\n"
                    f"💡 {reason}"
                )
                for i, (p, reason) in enumerate(zip(recommended, reasons))
            ]
            recommended_section = "\n\nRecommended Products:\n" + "\n\n".join(formatted_recommended)
            response += "\n\n" + recommended_section

        instructions = (
            "\n\nWhat would you like to do next?\n"
            "Type 'refine <query>' to refine your search,\n"
            "or 'add <product name>' to add another item to your cart,\n"
            "or 'view cart' to see your cart,\n"
            "or 'checkout' to proceed to checkout."
        )
        await cl.Message(content=response + instructions).send()
        cl.user_session.set("stage", "awaiting_query")
