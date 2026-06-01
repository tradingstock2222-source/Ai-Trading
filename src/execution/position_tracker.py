import psycopg2
from src.execution.schemas import ExecutionReport
from src.config import settings

class PositionTracker:
    def __init__(self):
        self.conn = psycopg2.connect(settings.DATABASE_URL)

    def update(self, exec: ExecutionReport):
        sign = 1 if exec.side.value == "BUY" else -1
        qty_delta = exec.quantity * sign
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO positions.positions (symbol, exchange, net_qty, avg_price)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (symbol, exchange) DO UPDATE
                SET net_qty = positions.net_qty + %s,
                    avg_price = CASE
                        WHEN positions.net_qty + %s = 0 THEN 0
                        ELSE (positions.avg_price * positions.net_qty + %s * %s) / (positions.net_qty + %s)
                    END,
                    updated_at = NOW()
            """, (
                exec.symbol, exec.exchange,
                qty_delta, exec.price,
                qty_delta,
                qty_delta,
                exec.price, exec.quantity,
                qty_delta
            ))
            self.conn.commit()
