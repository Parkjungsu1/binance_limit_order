# 🚀 Binance Limit Order Trading App

desktop trading application for Binance Futures
that prioritizes **limit orders over market orders** using real-time data.

Binance USDT-M Futures has the following basic fee structure:

| Type                 | Fee    | Description                                                       |
| -------------------- | ------ | ----------------------------------------------------------------- |
| Maker (Limit Order)  | 0.020% | Orders placed on the order book waiting to be filled              |
| Taker (Market Order) | 0.050% | Orders that are executed immediately by taking existing liquidity |

## Features

- 🔄 Real-time price tracking using WebSocket
- 📊 Live PnL calculation (USDT & KRW)
- ⚡ Strategy-based limit order execution
- 🖥️ Desktop UI built with PyQt5

## 🛠️ Tech Stack

- Python
- PyQt5
- Binance Futures API
- WebSocket
- REST API

## ⚙️ Setup

```bash
git clone https://github.com/Parkjungsu1/binance_limit_order.git
cd binance_limit_order

python -m venv venv
source venv/bin/activate  # mac
pip install -r requirements.txt

python main.py
```
