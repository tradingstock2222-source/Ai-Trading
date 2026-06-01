import asyncio
import logging
from datetime import datetime
from src.execution.schemas import Order, OrderStatus, ExecutionReport
from src.execution.broker_adapter import AbstractBrokerAdapter
from src.execution.pre_trade_risk import PreTradeRisk
from src.execution.safety import SafetyManager
from src.execution.trade_audit import AuditLogger
from src.execution.execution_recorder import ExecutionRecorder
from src.execution.position_tracker import PositionTracker

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, broker: AbstractBrokerAdapter, risk: PreTradeRisk,
                 safety: SafetyManager, audit: AuditLogger,
                 exec_recorder: ExecutionRecorder, pos_tracker: PositionTracker):
        self.broker = broker
        self.risk = risk
        self.safety = safety
        self.audit = audit
        self.exec_recorder = exec_recorder
        self.pos_tracker = pos_tracker
        self.orders = {}

    async def handle_new_order(self, order: Order):
        self.audit.log(order.order_id, "CREATED", order.dict())
        if not self.risk.validate(order, self.safety):
            order.status = OrderStatus.REJECTED
            order.updated_at = datetime.utcnow()
            self.audit.log(order.order_id, "REJECTED", {"reason": "Risk or safety check failed"})
            return order
        order.status = OrderStatus.VALIDATED
        order.updated_at = datetime.utcnow()
        self.audit.log(order.order_id, "VALIDATED", order.dict())
        broker_order_id = await self.broker.submit_order(order)
        order.status = OrderStatus.ROUTED
        order.updated_at = datetime.utcnow()
        self.audit.log(order.order_id, "ROUTED", {"broker_id": broker_order_id})
        self.orders[order.order_id] = order
        return order

    async def on_execution_report(self, exec_rpt: ExecutionReport):
        order = self.orders.get(exec_rpt.order_id)
        if not order:
            logger.warning(f"Execution for unknown order {exec_rpt.order_id}")
            return
        order.filled_qty += exec_rpt.quantity
        order.avg_price = (
            ((order.avg_price or 0) * (order.filled_qty - exec_rpt.quantity) + exec_rpt.price * exec_rpt.quantity)
            / order.filled_qty
        )
        order.updated_at = datetime.utcnow()
        if order.filled_qty >= order.quantity:
            order.status = OrderStatus.FILLED
        else:
            order.status = OrderStatus.PARTIAL
        self.audit.log(order.order_id, "FILLED", exec_rpt.dict())
        self.exec_recorder.record(exec_rpt)
        self.pos_tracker.update(exec_rpt)
