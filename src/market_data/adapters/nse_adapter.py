import asyncio
import random
from datetime import datetime, timezone

class NSEAdapter:
    def __init__(self):
        self.base_prices = {
            'RELIANCE': 2500.0,
            'TCS': 3500.0,
            'INFY': 1500.0,
            'HDFCBANK': 1600.0
        }

    async def subscribe(self, symbols: list):
        prices = {sym: self.base_prices.get(sym, 1000.0) for sym in symbols}
        while True:
            for sym in symbols:
                price_change = random.gauss(0, 2)
                prices[sym] = max(prices[sym] + price_change, 0.01)
                tick = {
                    'time': datetime.now(timezone.utc).isoformat(),
                    'symbol': sym,
                    'last_price': round(prices[sym], 2),
                    'volume': random.randint(100, 10000),
                    'bid': round(prices[sym] - 0.5, 2),
                    'ask': round(prices[sym] + 0.5, 2),
                    'bid_qty': random.randint(1000, 50000),
                    'ask_qty': random.randint(1000, 50000),
                    'exchange': 'NSE'
                }
                yield tick
            await asyncio.sleep(0.5)
