import argparse
import json
import logging
import os
import sys

from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot import orders

setup_logging()
logger = logging.getLogger(__name__)

def _sep(char="─", width=60):
    print(char * width)

def _print_summary(summary):
    _sep()
    print("  ORDER REQUEST SUMMARY")
    _sep()
    for k, v in summary.items():
        print(f"  {k:<14}: {v}")
    _sep()

def _print_response(response):
    _sep()
    print("  ORDER RESPONSE")
    _sep()
    fields = [
        ("orderId","Order ID"),("status","Status"),("symbol","Symbol"),
        ("side","Side"),("type","Type"),("origQty","Orig Qty"),
        ("executedQty","Executed Qty"),("avgPrice","Avg Price"),
        ("price","Price"),("stopPrice","Stop Price"),("updateTime","Update Time"),
    ]
    for key, label in fields:
        if key in response:
            print(f"  {label:<14}: {response[key]}")
    _sep()
    print("\n  Full response (JSON):")
    print(json.dumps(response, indent=4))
    _sep()

def build_parser():
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance USDT-M Futures Testnet",
    )
    parser.add_argument("--symbol",     required=True)
    parser.add_argument("--side",       required=True)
    parser.add_argument("--type",       required=True, dest="order_type")
    parser.add_argument("--quantity",   required=True)
    parser.add_argument("--price",      required=False, default=None)
    parser.add_argument("--stop-price", required=False, default=None, dest="stop_price")
    return parser

def main():
    load_dotenv()
    api_key    = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print("\n  ERROR: API credentials not found.")
        print("  Create a .env file with BINANCE_API_KEY and BINANCE_API_SECRET.\n")
        sys.exit(1)

    parser = build_parser()
    args   = parser.parse_args()

    logger.info("CLI invoked — symbol=%s side=%s type=%s qty=%s price=%s stop_price=%s",
        args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price)

    try:
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
    except ValueError as exc:
        print(f"\n  ERROR: {exc}\n")
        sys.exit(1)

    print()
    result = orders.place_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price,
    )

    if result["summary"]:
        _print_summary(result["summary"])

    if result["success"]:
        _print_response(result["response"])
        print("\n  SUCCESS: Order placed successfully!\n")
        logger.info("Order placed successfully — orderId: %s", result["response"].get("orderId"))
    else:
        print(f"\n  FAILED: {result['error']}\n")
        logger.error("Order failed: %s", result["error"])
        sys.exit(1)

if __name__ == "__main__":
    main()
