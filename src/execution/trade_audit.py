import psycopg2
import json
from src.config import settings

class AuditLogger:
    def __init__(self):
        self.conn = psycopg2.connect(settings.DATABASE_URL)

    def log(self, order_id: str, event_type: str, data: dict):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders.order_events (order_id, event_type, event_data)
                VALUES (%s, %s, %s)
            """, (order_id, event_type, json.dumps(data, default=str)))
            self.conn.commit()
