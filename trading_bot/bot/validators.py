from decimal import Decimal, InvalidOperation


class ValidationError(Exception):
    pass


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValidationError("Symbol is required.")
    symbol = symbol.strip().upper()
    if not symbol.endswith("USDT"):
        raise ValidationError("Only USDT-M symbols are supported, e.g. BTCUSDT.")
    if len(symbol) < 6:
        raise ValidationError("Invalid symbol format.")
    return symbol


def validate_side(side: str) -> str:
    if not side:
        raise ValidationError("Side is required.")
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValidationError("Order type is required.")
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return order_type


def validate_quantity(quantity: str) -> str:
    if quantity is None:
        raise ValidationError("Quantity is required.")
    try:
        q = Decimal(str(quantity))
        if q <= 0:
            raise ValidationError("Quantity must be greater than 0.")
    except (InvalidOperation, ValueError):
        raise ValidationError("Quantity must be a valid positive number.")
    return str(q.normalize())


def validate_price(price: str, order_type: str) -> str | None:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            p = Decimal(str(price))
            if p <= 0:
                raise ValidationError("Price must be greater than 0.")
        except (InvalidOperation, ValueError):
            raise ValidationError("Price must be a valid positive number.")
        return str(p.normalize())
    return None
