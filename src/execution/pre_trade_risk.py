from src.execution.schemas import Order
from src.execution.safety import SafetyManager

class PreTradeRisk:
    def __init__(self, max_order_value: float = 1e6, max_position: int = 100000):
        self.max_order_value = max_order_value
        self.max_position = max_position

    def validate(self, order: Order, safety: SafetyManager) -> bool:
        if not safety.trading_allowed(order.symbol):
            return False

        if order.quantity <= 0:
            return False
        if order.price is not None and order.price <= 0:
            return False
        if order.price and order.quantity * order.price > self.max_order_value:
            return False
        return True
