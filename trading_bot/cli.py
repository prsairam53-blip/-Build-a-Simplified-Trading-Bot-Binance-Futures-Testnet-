import argparse
import sys

from dotenv import load_dotenv

from bot.client import (
    BinanceAPIError,
    BinanceFuturesTestnetClient,
    BinanceNetworkError,
    load_credentials,
)
from bot.logging_config import setup_logger
from bot.orders import build_order_payload, format_order_response, summarize_order
from bot.validators import ValidationError


def parse_args():
    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Price for LIMIT orders")
    return parser.parse_args()


def main():
    load_dotenv()
    logger = setup_logger()

    try:
        args = parse_args()
        api_key, api_secret, base_url = load_credentials()

        client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            logger=logger,
        )

        payload = build_order_payload(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        print(summarize_order(payload))
        print("-" * 50)

        client.ping()
        response = client.place_order(payload)

        print(format_order_response(response))
        print("-" * 50)
        print("Success: Order placed successfully.")

    except ValidationError as exc:
        logger.exception("Validation error")
        print(f"Failure: Validation error - {exc}")
        sys.exit(1)

    except ValueError as exc:
        logger.exception("Configuration error")
        print(f"Failure: Configuration error - {exc}")
        sys.exit(1)

    except BinanceAPIError as exc:
        logger.exception("Binance API error")
        print(f"Failure: API error - {exc}")
        sys.exit(1)

    except BinanceNetworkError as exc:
        logger.exception("Network failure")
        print(f"Failure: Network error - {exc}")
        sys.exit(1)

    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"Failure: Unexpected error - {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
