import asyncio
import json
import logging
from kafka import KafkaProducer
from src.config import settings
from src.market_data.adapters.nse_adapter import NSEAdapter
from src.market_data.adapters.bse_adapter import BSEAdapter

logger = logging.getLogger(__name__)

class MarketDataConnector:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = settings.KAFKA_TOPIC
        self.adapters = {
            'NSE': NSEAdapter(),
            'BSE': BSEAdapter()
        }

    async def stream(self, symbols: list, exchange: str = 'NSE'):
        adapter = self.adapters.get(exchange)
        if not adapter:
            raise ValueError(f"Unsupported exchange: {exchange}")
        async for tick in adapter.subscribe(symbols):
            self.producer.send(self.topic, value=tick)
            logger.info(f"Tick sent: {tick['symbol']}@{tick['time']}")

    async def run(self):
        await asyncio.gather(
            self.stream(['RELIANCE', 'TCS', 'INFY', 'HDFCBANK'], 'NSE'),
            self.stream(['500325', '532174'], 'BSE')
        )

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    connector = MarketDataConnector()
    asyncio.run(connector.run())
