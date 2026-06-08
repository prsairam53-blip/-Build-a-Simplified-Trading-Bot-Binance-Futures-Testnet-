# Binance Futures Testnet Trading Bot

A simplified Python CLI trading bot for Binance Futures Testnet (USDT-M) that supports MARKET and LIMIT orders for both BUY and SELL sides.

## Features

- Place MARKET orders
- Place LIMIT orders
- Supports BUY and SELL
- CLI input using argparse
- Input validation
- Structured codebase
- Logging of API requests, responses, and errors
- Error handling for validation, API, and network failures

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── logs/
├── .env.example
├── cli.py
├── README.md
└── requirements.txt
```

## Setup

1. Clone the repository or extract the archive.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`
5. Add your Binance Futures Testnet API credentials in `.env`

## Environment Variables

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

## Run Examples

### MARKET BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### MARKET SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type MARKET --quantity 0.001
```

### LIMIT BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.001 --price 50000
```

### LIMIT SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 90000
```

## Output

The app prints:

- Order request summary
- Order response details:
  - orderId
  - status
  - executedQty
  - avgPrice (if available)
- Success or failure message

## Logging

Logs are stored in the `logs/` directory.

The logger records:

- API requests
- API responses
- Validation errors
- Network failures
- Unexpected exceptions

## Assumptions

- Only USDT-M Binance Futures Testnet is targeted.
- Symbols are entered manually, e.g. `BTCUSDT`.
- LIMIT orders are sent with `timeInForce=GTC`.
- Quantity and price precision depend on Binance symbol rules; if precision is invalid, Binance will reject the order and the app will show the API error.

## Notes

- Use only Binance Futures Testnet credentials, not production credentials.
- Ensure your testnet account is activated and funded with test assets if required.
