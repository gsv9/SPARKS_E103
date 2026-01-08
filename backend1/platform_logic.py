import json
from api_clients.serpapi_client import search_products

# Load platform links
with open("links.json", "r") as f:
    LINKS = json.load(f)

pending_compare = False
pending_nav = None


def process_message(message):
    global pending_compare, pending_nav

    msg = message.lower().strip()

    # =========================
    # 1️⃣ PRODUCT COMPARISON
    # =========================
    if msg.startswith("compare"):
        pending_compare = True
        pending_nav = None

        product = msg.replace("compare", "", 1).strip()
        if not product:
            return {"text": "Please specify a product. Example: compare iphone 14"}

        results = search_products(product)

        amazon = None
        flipkart = None

        for item in results:
            source = (item.get("source") or "").lower()
            if "amazon" in source and not amazon:
                amazon = item
            elif "flipkart" in source and not flipkart:
                flipkart = item

        response = f"Comparison for {product.title()}:\n\n"

        response += (
            f"Amazon:\n• Price: {amazon.get('price') if amazon else 'Unavailable'}\n\n"
            f"Flipkart:\n• Price: {flipkart.get('price') if flipkart else 'Unavailable'}\n\n"
        )

        response += "Which platform do you want to open? (Amazon / Flipkart)"

        return {"text": response}

    # =========================
    # 2️⃣ PLATFORM SELECTION AFTER COMPARISON
    # =========================
    if pending_compare and msg in ["amazon", "flipkart"]:
        pending_compare = False
        return {
            "text": f"Opening {msg.title()}",
            "redirect_url": LINKS[msg.capitalize()]["home"]
        }

    # =========================
    # 3️⃣ CART
    # =========================
    if "cart" in msg:
        pending_nav = "cart"
        pending_compare = False
        return {"text": "Which platform? (Amazon / Flipkart)"}

    # =========================
    # 4️⃣ ORDERS
    # =========================
    if "order" in msg or "track" in msg:
        pending_nav = "orders"
        pending_compare = False
        return {"text": "Which platform? (Amazon / Flipkart)"}

    # =========================
    # 5️⃣ WISHLIST
    # =========================
    if "wishlist" in msg:
        pending_nav = "wishlist"
        pending_compare = False
        return {"text": "Which platform? (Amazon / Flipkart)"}

    # =========================
    # 6️⃣ PROFILE
    # =========================
    if "profile" in msg or "account" in msg:
        pending_nav = "profile"
        pending_compare = False
        return {"text": "Which platform? (Amazon / Flipkart)"}

    # =========================
    # 7️⃣ PLATFORM SELECTION FOR NAVIGATION
    # =========================
    if pending_nav and msg in ["amazon", "flipkart"]:
        action = pending_nav
        pending_nav = None
        return {
            "text": f"Opening {action} on {msg.title()}",
            "redirect_url": LINKS[msg.capitalize()][action]
        }

    # =========================
    # 8️⃣ DEFAULT
    # =========================
    return {
        "text": (
            "I can help you with:\n"
            "• Compare products\n"
            "• Open cart\n"
            "• Track orders\n"
            "• View wishlist\n"
            "• Open profile\n\n"
            "Example: compare samsung galaxy s24"
        )
    }