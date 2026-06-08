from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)


def build_order_payload(symbol: str, side: str, order_type: str, quantity: str, price: str | None = None) -> dict:
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)

    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"

    return payload


def summarize_order(payload: dict) -> str:
    lines = [
        "Order Request Summary",
        f"Symbol     : {payload.get('symbol')}",
        f"Side       : {payload.get('side')}",
        f"Type       : {payload.get('type')}",
        f"Quantity   : {payload.get('quantity')}",
    ]

    if payload.get("type") == "LIMIT":
        lines.append(f"Price      : {payload.get('price')}")
        lines.append(f"TimeInForce: {payload.get('timeInForce')}")

    return "\n".join(lines)


def format_order_response(response: dict) -> str:
    return "\n".join(
        [
            "Order Response Details",
            f"orderId     : {response.get('orderId')}",
            f"symbol      : {response.get('symbol')}",
            f"status      : {response.get('status')}",
            f"side        : {response.get('side')}",
            f"type        : {response.get('type')}",
            f"origQty     : {response.get('origQty')}",
            f"executedQty : {response.get('executedQty')}",
            f"price       : {response.get('price')}",
            f"avgPrice    : {response.get('avgPrice')}",
        ]
    )
