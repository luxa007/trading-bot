from decimal import Decimal, InvalidOperation
from typing import Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}

def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValueError("Symbol must not be empty.")
    if not s.isalnum():
        raise ValueError(f"Symbol '{s}' must be alphanumeric, e.g. BTCUSDT.")
    return s

def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, got '{side}'.")
    return s

def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be MARKET, LIMIT, or STOP_MARKET — got '{order_type}'.")
    return t

def validate_quantity(quantity) -> str:
    try:
        q = Decimal(str(quantity))
    except InvalidOperation:
        raise ValueError(f"Quantity '{quantity}' is not a valid number.")
    if q <= 0:
        raise ValueError(f"Quantity must be positive, got {q}.")
    return f"{q:f}"

def validate_price(price, order_type: str) -> Optional[str]:
    if order_type == "MARKET":
        return None
    if price is None or str(price).strip() == "":
        raise ValueError(f"Price is required for {order_type} orders. Use --price.")
    try:
        p = Decimal(str(price))
    except InvalidOperation:
        raise ValueError(f"Price '{price}' is not a valid number.")
    if p <= 0:
        raise ValueError(f"Price must be positive, got {p}.")
    return f"{p:f}"

def validate_stop_price(stop_price, order_type: str) -> Optional[str]:
    if order_type != "STOP_MARKET":
        return None
    if stop_price is None or str(stop_price).strip() == "":
        raise ValueError("Stop price is required for STOP_MARKET orders. Use --stop-price.")
    try:
        sp = Decimal(str(stop_price))
    except InvalidOperation:
        raise ValueError(f"Stop price '{stop_price}' is not a valid number.")
    if sp <= 0:
        raise ValueError(f"Stop price must be positive, got {sp}.")
    return f"{sp:f}"
