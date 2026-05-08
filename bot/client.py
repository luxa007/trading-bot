"""
Binance Futures Testnet - API Client Layer
"""
import hashlib
import hmac
import time
import logging
from typing import Optional
from urllib.parse import urlencode
import requests

logger = logging.getLogger(__name__)
TESTNET_BASE_URL = "https://testnet.binancefuture.com"

class BinanceClientError(Exception):
    pass

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = TESTNET_BASE_URL):
        if not api_key or not api_secret:
            raise ValueError("API key and secret must not be empty.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })
        logger.info("BinanceFuturesClient initialised — base URL: %s", self.base_url)

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _handle_response(self, response: requests.Response) -> dict:
        try:
            data = response.json()
        except Exception:
            raise BinanceClientError(
                f"Non-JSON response (HTTP {response.status_code}): {response.text[:200]}"
            )
        if isinstance(data, dict) and "code" in data and int(data["code"]) < 0:
            raise BinanceClientError(f"API Error {data['code']}: {data.get('msg', 'Unknown error')}")
        if response.status_code != 200:
            raise BinanceClientError(f"HTTP {response.status_code}: {response.text[:200]}")
        logger.debug("Response: %s", data)
        return data

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None, time_in_force="GTC"):
        url = f"{self.base_url}/fapi/v1/order"
        order_type = order_type.upper()
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type,
            "quantity": quantity,
            "newOrderRespType": "RESULT",
        }
        if order_type == "LIMIT":
            if not price:
                raise BinanceClientError("Price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force
        if order_type == "STOP_MARKET":
            if not stop_price:
                raise BinanceClientError("stopPrice is required for STOP_MARKET orders.")
            params["stopPrice"] = stop_price
        logger.info("Placing order — request params: %s", params)
        signed = self._sign(params)
        try:
            response = self.session.post(url, data=signed, timeout=10)
        except requests.exceptions.ConnectionError as exc:
            raise BinanceClientError(f"Network error: {exc}") from exc
        except requests.exceptions.Timeout as exc:
            raise BinanceClientError("Request timed out.") from exc
        result = self._handle_response(response)
        logger.info("Order response: %s", result)
        return result

    def get_account(self) -> dict:
        url = f"{self.base_url}/fapi/v2/account"
        params = self._sign({})
        logger.info("Fetching account info")
        response = self.session.get(url, params=params, timeout=10)
        return self._handle_response(response)
