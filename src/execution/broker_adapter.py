from abc import ABC, abstractmethod
from typing import AsyncIterator
from src.execution.schemas import Order, ExecutionReport
from datetime import datetime

class AbstractBrokerAdapter(ABC):
    @abstractmethod
    async def submit_order(self, order: Order) -> str:
        """Submit order, return broker order ID."""
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        pass

    @abstractmethod
    async def modify_order(self, order_id: str, new_qty: int, new_price: float) -> bool:
        pass

    @abstractmethod
    async def stream_executions(self) -> AsyncIterator[ExecutionReport]:
        """Stream execution reports asynchronously."""
        pass

class MockBrokerAdapter(AbstractBrokerAdapter):
    def __init__(self):
        import asyncio
        self.orders = {}
        self.exec_queue = asyncio.Queue()

    async def submit_order(self, order: Order) -> str:
        broker_id = f"broker-{order.client_order_id or order.order_id}"
        self.orders[broker_id] = order
        if order.order_type == "MARKET":
            exec_report = ExecutionReport(
                order_id=order.order_id,
                symbol=order.symbol,
                exchange=order.exchange,
                side=order.side,
                quantity=order.quantity,
                price=100.0,
                exec_time=datetime.utcnow()
            )
            await self.exec_queue.put(exec_report)
        return broker_id

    async def cancel_order(self, order_id: str) -> bool:
        return True

    async def modify_order(self, order_id: str, new_qty: int, new_price: float) -> bool:
        return True

    async def stream_executions(self):
        while True:
            exec_rpt = await self.exec_queue.get()
            yield exec_rpt
