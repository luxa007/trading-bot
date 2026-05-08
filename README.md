# Trading Bot – Binance Futures Testnet

A simplified Python trading bot for Binance USDT-M Futures Testnet.

## Features

- Place MARKET orders
- Place LIMIT orders
- BUY and SELL support
- CLI input using argparse
- Input validation
- Logging to file
- Error handling
- Structured reusable code

## Project Structure

```text
trading_bot/
│
├── bot/
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│   └── trading_bot.log
│
├── cli.py
├── requirements.txt
├── README.md
└── .env
```

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/luxa007/trading-bot.git
cd trading-bot
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

## Binance Futures Testnet

Base URL used:

```text
https://testnet.binancefuture.com
```

## Example Commands

### MARKET Order

```bash
python cli.py \
--symbol BTCUSDT \
--side BUY \
--type MARKET \
--quantity 0.001
```

### LIMIT Order

```bash
python cli.py \
--symbol BTCUSDT \
--side SELL \
--type LIMIT \
--quantity 0.001 \
--price 120000
```

## Logging

Logs are stored in:

```text
logs/trading_bot.log
```

The application logs:
- API requests
- API responses
- Errors
- CLI activity

## Assumptions

- Binance Futures Testnet account is active
- API credentials are valid
- User has sufficient testnet balance

## Requirements

- Python 3.x
- requests
- python-dotenv

## Author

Tinotenda Luciano# trading-bot
