import asyncio
import random
from datetime import datetime, timezone

class BSEAdapter:
    def __init__(self):
        self.base_prices = {
            '500325': 2500.0,
            '532174': 1050.0
        }

    async def subscribe(self, symbols: list):
        prices = {sym: self.base_prices.get(sym, 500.0) for sym in symbols}
        while True:
            for sym in symbols:
                price_change = random.gauss(0, 1.5)
                prices[sym] = max(prices[sym] + price_change, 0.01)
                tick = {
                    'time': datetime.now(timezone.utc).isoformat(),
                    'symbol': sym,
                    'last_price': round(prices[sym], 2),
                    'volume': random.randint(100, 8000),
                    'bid': round(prices[sym] - 0.3, 2),
                    'ask': round(prices[sym] + 0.3, 2),
                    'bid_qty': random.randint(500, 30000),
                    'ask_qty': random.randint(500, 30000),
                    'exchange': 'BSE'
                }
                yield tick
            await asyncio.sleep(0.6)
