import logging
from src.execution.position_tracker import PositionTracker
from src.execution.broker_adapter import AbstractBrokerAdapter

logger = logging.getLogger(__name__)

class ReconciliationEngine:
    def __init__(self, position_tracker: PositionTracker, broker: AbstractBrokerAdapter):
        self.pos_tracker = position_tracker
        self.broker = broker

    async def reconcile(self):
        logger.info("Reconciliation ran: all positions match (mock)")
