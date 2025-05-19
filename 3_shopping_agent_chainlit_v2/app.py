import os, json, tempfile, sys, re
import chainlit as cl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google credentials handling
gc_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if gc_json:
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(gc_json)

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name


# Add 'src' to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from chainlit_shopping_agent.shopping_agents import shopping_manager
from chainlit_shopping_agent.config_agents import config
from agents import Runner

# In-memory session
session = {"cart": [], "last_search_results": [], "last_recommended": []}

def extract_search_result(response):
    if isinstance(response, dict):
        return response
    try:
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
    except:
        pass
    try:
        return json.loads(response)
    except:
        return {"products": [], "recommended_products": []}

def format_products(result):
    products = result.get("products", [])
    recommended = result.get("recommended_products", [])
    message = result.get("message", "")
    text = f"### {message}\n\n"

    if products:
        text += "**Matching Products:**\n"
        for i, p in enumerate(products, 1):
            text += f"{i}. **{p['name']}** - ${p['price']}, Rating: {p['rating']}, Stock: {p['stock']}\n{p['description']}\n\n"
    else:
        text += "No products found.\n"

    if recommended:
        text += "**Recommended Products:**\n"
        for p in recommended:
            text += f"- **{p['name']}** - ${p['price']} (Rating: {p['rating']})\n"

    return text.strip()

@cl.on_chat_start
async def start():
    cl.user_session.set("session", session)
    await cl.Message(content="👋 Welcome to the Furniture Shopping Assistant! Type your search or ask for help.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    content = message.content.strip().lower()
    session = cl.user_session.get("session")

    msg = cl.Message(content="")

    reply = ""

    if content.startswith("refine "):
        query = content[7:].strip()
        if not query:
            reply = "❗ Please provide a search term after `refine`."
        else:
            response = Runner.run_sync(shopping_manager, query, run_config=config).final_output
            result = extract_search_result(response)
            session["last_search_results"] = result.get("products", [])
            session["last_recommended"] = result.get("recommended_products", [])
            reply = format_products(result)

    elif content.startswith("add "):
        name = content[4:].strip()
        found = next((p for p in session["last_search_results"] + session["last_recommended"]
                      if name.lower() in p["name"].lower()), None)
        if found:
            session["cart"].append(found)
            reply = f"✅ Added **{found['name']}** to your cart. Cart has {len(session['cart'])} item(s)."
        else:
            reply = f"❌ Could not find product matching '{name}'."

    elif content == "view cart":
        if not session["cart"]:
            reply = "🛒 Your cart is empty."
        else:
            total = sum(p["price"] for p in session["cart"])
            reply = "**🛒 Your Cart:**\n\n"
            for i, p in enumerate(session["cart"], 1):
                reply += f"{i}. **{p['name']}** - ${p['price']}\n"
            reply += f"\n**Total:** ${total}"

    elif content == "checkout":
        if not session["cart"]:
            reply = "Your cart is empty. Add some items first!"
        else:
            total = sum(p["price"] for p in session["cart"])
            reply = "**✅ Checkout Summary**\n\n"
            for i, p in enumerate(session["cart"], 1):
                reply += f"{i}. {p['name']} - ${p['price']}\n"
            reply += f"\n**Total: ${total}**\nThanks for shopping with us!"
            session["cart"] = []

    else:
        response = Runner.run_sync(shopping_manager, content, run_config=config).final_output
        result = extract_search_result(response)
        session["last_search_results"] = result.get("products", [])
        session["last_recommended"] = result.get("recommended_products", [])
        reply = format_products(result)

    reply += "\n\nWhat would you like to do next?\n- `refine <query>` to search again\n- `add <product>` to add to cart\n- `view cart` or `checkout`"
    await msg.stream_token(reply)
    await msg.send()
