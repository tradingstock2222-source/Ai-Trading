import asyncio
import logging
import uvicorn
from src.execution.broker_adapter import MockBrokerAdapter
from src.execution.pre_trade_risk import PreTradeRisk
from src.execution.safety import SafetyManager
from src.execution.trade_audit import AuditLogger
from src.execution.execution_recorder import ExecutionRecorder
from src.execution.position_tracker import PositionTracker
from src.execution.order_manager import OrderManager
from src.execution.reconciliation import ReconciliationEngine
from src.execution.api import app, set_managers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    broker = MockBrokerAdapter()
    risk = PreTradeRisk(max_order_value=1e7, max_position=100000)
    safety = SafetyManager()
    audit = AuditLogger()
    exec_recorder = ExecutionRecorder()
    pos_tracker = PositionTracker()

    order_manager = OrderManager(broker, risk, safety, audit, exec_recorder, pos_tracker)
    reconciliation = ReconciliationEngine(pos_tracker, broker)

    set_managers(order_manager, safety)

    async def execution_listener():
        async for exec_rpt in broker.stream_executions():
            await order_manager.on_execution_report(exec_rpt)

    async def reconciliation_loop():
        while True:
            await reconciliation.reconcile()
            await asyncio.sleep(5)

    asyncio.create_task(execution_listener())
    asyncio.create_task(reconciliation_loop())

    config = uvicorn.Config(app, host="0.0.0.0", port=8001, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
