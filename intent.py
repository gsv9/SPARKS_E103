def detect_intent(message):
    msg = message.lower()

    if "compare" in msg or "cheaper" in msg:
        return "compare"

    if "cart" in msg:
        return "cart"

    if "wishlist" in msg or "saved" in msg:
        return "wishlist"

    if "order" in msg or "orders" in msg or "track" in msg:
        return "orders"

    if "profile" in msg or "account" in msg:
        return "profile"

    return "unknown"
