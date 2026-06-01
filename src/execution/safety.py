import time
from enum import Enum

class KillSwitchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ENGAGED = "ENGAGED"

class SafetyManager:
    def __init__(self):
        self.kill_switch = KillSwitchStatus.ACTIVE
        self.circuit_breaker_tripped = False
        self.daily_pnl_limit = -50000.0
        self.current_pnl = 0.0
        self.last_broker_heartbeat = time.time()

    def trading_allowed(self, symbol: str = None) -> bool:
        if self.kill_switch == KillSwitchStatus.ENGAGED:
            return False
        if self.circuit_breaker_tripped:
            return False
        if time.time() - self.last_broker_heartbeat > 5:
            return False
        return True

    def update_pnl(self, pnl: float):
        self.current_pnl = pnl
        if self.current_pnl <= self.daily_pnl_limit:
            self.circuit_breaker_tripped = True

    def engage_kill_switch(self):
        self.kill_switch = KillSwitchStatus.ENGAGED

    def reset_kill_switch(self):
        self.kill_switch = KillSwitchStatus.ACTIVE
        self.circuit_breaker_tripped = False

    def heartbeat_received(self):
        self.last_broker_heartbeat = time.time()
