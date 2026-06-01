import psycopg2
from src.execution.schemas import ExecutionReport
from src.config import settings

class ExecutionRecorder:
    def __init__(self):
        self.conn = psycopg2.connect(settings.DATABASE_URL)

    def record(self, report: ExecutionReport):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders.executions (exec_id, order_id, symbol, exchange, side, quantity, price, commission, exec_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                report.exec_id, report.order_id, report.symbol, report.exchange,
                report.side.value, report.quantity, report.price, report.commission, report.exec_time
            ))
            self.conn.commit()
