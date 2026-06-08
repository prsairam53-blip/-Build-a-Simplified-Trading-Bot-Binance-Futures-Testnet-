import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import requests


class BinanceAPIError(Exception):
    pass


class BinanceNetworkError(Exception):
    pass


class BinanceFuturesTestnetClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str, logger):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(self, method: str, endpoint: str, params: dict | None = None, signed: bool = False):
        params = params or {}
        url = f"{self.base_url}{endpoint}"

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000
            params["signature"] = self._sign(params)

        self.logger.info("API Request | method=%s | url=%s | params=%s", method, url, params)

        try:
            response = self.session.request(method=method, url=url, params=params, timeout=15)
            self.logger.info(
                "API Response | status_code=%s | body=%s",
                response.status_code,
                response.text,
            )
        except requests.RequestException as exc:
            self.logger.exception("Network error during Binance API request.")
            raise BinanceNetworkError(str(exc)) from exc

        try:
            data = response.json()
        except ValueError:
            raise BinanceAPIError(f"Non-JSON response from API: {response.text}")

        if response.status_code >= 400:
            msg = data.get("msg", "Unknown Binance API error")
            code = data.get("code", "N/A")
            raise BinanceAPIError(f"Binance API Error | code={code} | message={msg}")

        return data

    def ping(self):
        return self._request("GET", "/fapi/v1/ping")

    def place_order(self, payload: dict):
        return self._request("POST", "/fapi/v1/order", params=payload, signed=True)


def load_credentials():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET environment variables.")

    return api_key, api_secret, base_url
