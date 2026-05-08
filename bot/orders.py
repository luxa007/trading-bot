import logging
from typing import Optional
from bot.client import BinanceFuturesClient, BinanceClientError
from bot import validators

logger = logging.getLogger(__name__)

def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    try:
        sym  = validators.validate_symbol(symbol)
        sid  = validators.validate_side(side)
        otyp = validators.validate_order_type(order_type)
        qty  = validators.validate_quantity(quantity)
        prc  = validators.validate_price(price, otyp)
        stp  = validators.validate_stop_price(stop_price, otyp)
    except ValueError as exc:
        logger.warning("Validation error: %s", exc)
        return {"success": False, "summary": {}, "response": None, "error": str(exc)}

    summary = {"symbol": sym, "side": sid, "type": otyp, "quantity": qty}
    if prc:
        summary["price"] = prc
    if stp:
        summary["stopPrice"] = stp
    logger.info("Order request summary: %s", summary)

    try:
        response = client.place_order(
            symbol=sym, side=sid, order_type=otyp,
            quantity=qty, price=prc, stop_price=stp,
        )
    except BinanceClientError as exc:
        logger.error("API error: %s", exc)
        return {"success": False, "summary": summary, "response": None, "error": str(exc)}
    except Exception as exc:
        logger.error("Unexpected error: %s", exc, exc_info=True)
        return {"success": False, "summary": summary, "response": None, "error": f"Unexpected error: {exc}"}

    return {"success": True, "summary": summary, "response": response, "error": None}
