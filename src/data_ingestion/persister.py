import json
import logging
import psycopg2
from kafka import KafkaConsumer
from src.config import settings
from src.data_validation.validator import validate_tick
from src.monitoring.data_quality import (
    ticks_ingested, ticks_validated, validation_failures
)

logger = logging.getLogger(__name__)

def persist_ticks():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()

    logger.info("Starting tick persister...")
    for message in consumer:
        tick = message.value
        ticks_ingested.inc()

        if not validate_tick(tick):
            validation_failures.inc()
            continue

        ticks_validated.inc()

        table = f"ticks_{tick['exchange'].lower()}"
        try:
            cur.execute(f"""
                INSERT INTO market_data.{table}
                (time, symbol, last_price, volume, bid, ask, bid_qty, ask_qty, exchange)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                tick['time'], tick['symbol'], tick['last_price'], tick['volume'],
                tick.get('bid'), tick.get('ask'), tick.get('bid_qty'), tick.get('ask_qty'),
                tick['exchange']
            ))
            conn.commit()
        except Exception as e:
            logger.error(f"DB insert failed: {e}")
            conn.rollback()
    cur.close()
    conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    persist_ticks()
