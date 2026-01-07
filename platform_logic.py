from data_loader import load_data

products = load_data("products.json")
cart = load_data("cart.json")
wishlist = load_data("wishlist.json")
orders = load_data("orders.json")
links = load_data("links.json")

pending_action = None


def process_message(intent, message):
    global pending_action
    message = message.lower().strip()

    platforms = ["amazon", "flipkart", "myntra"]

    # 1️⃣ Handle platform selection if waiting
    if pending_action:
        if message in platforms:
            platform = message.capitalize()
            action = pending_action
            pending_action = None

            if action == "orders":
                user_orders = orders.get(platform, [])

                if not user_orders:
                    return {
                        "text": f"You have no orders on {platform}."
                    }

                undelivered = [
                    o for o in user_orders
                    if o["status"].lower() != "delivered"
                ]

                if not undelivered:
                    return {
                        "text": f"All your orders on {platform} are delivered. Do you want to open the orders page?",
                        "redirect_url": links[platform]["orders"]
                    }

                order_list = "\n".join(
                    [f"- {o['item']} ({o['status']})" for o in undelivered]
                )

                return {
                    "text": (
                        f"You have {len(undelivered)} active order(s) on {platform}:\n"
                        f"{order_list}\n\n"
                        "Do you want to open the orders page?"
                    ),
                    "redirect_url": links[platform]["orders"]
                }

            return {
                "text": f"Do you want me to open your {platform} {action}?",
                "redirect_url": links[platform][action]
            }

        # Still waiting for platform name
        return {
            "text": "Please choose a platform: Amazon, Flipkart, or Myntra."
        }

    # 2️⃣ Normal intent handling
    if intent == "compare":
        product = "iphone_14"
        data = products[product]

        best_platform = min(data, key=lambda p: data[p]["price"])

        platform_map = {
            "amazon": "Amazon",
            "flipkart": "Flipkart",
            "myntra": "Myntra"
        }

        platform_key = platform_map[best_platform.lower()]
        price = data[best_platform]["price"]

        return {
            "text": f"{platform_key} has the best price at ₹{price}. Do you want to open the iPhone 14 product page?",
            "redirect_url": links[platform_key]["iphone_14"]
        }

    if intent == "cart":
        pending_action = "cart"
        return {
            "text": "Which platform do you want to check your cart on?"
        }

    if intent == "wishlist":
        pending_action = "wishlist"
        return {
            "text": "Which platform’s wishlist should I open?"
        }

    if intent == "orders":
        pending_action = "orders"
        return {
            "text": "Which platform do you want to track orders from?"
        }

    if intent == "profile":
        pending_action = "profile"
        return {
            "text": "Which platform profile should I open?"
        }

    return {
        "text": "Please tell me what you want to do: compare products, view cart, wishlist, orders, or profile."
    }
