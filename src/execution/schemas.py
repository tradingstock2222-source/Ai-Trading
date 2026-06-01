from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from enum import Enum
from typing import Optional

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    ROUTED = "ROUTED"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class OrderRequest(BaseModel):
    symbol: str
    exchange: str = "NSE"
    order_type: OrderType
    side: Side
    quantity: int
    price: Optional[float] = None
    client_order_id: Optional[str] = None

class Order(OrderRequest):
    order_id: str = Field(default_factory=lambda: str(uuid4()))
    status: OrderStatus = OrderStatus.PENDING
    filled_qty: int = 0
    avg_price: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ExecutionReport(BaseModel):
    exec_id: str = Field(default_factory=lambda: str(uuid4()))
    order_id: str
    symbol: str
    exchange: str
    side: Side
    quantity: int
    price: float
    commission: float = 0.0
    exec_time: datetime = Field(default_factory=datetime.utcnow)

class Position(BaseModel):
    symbol: str
    exchange: str
    net_qty: int
    avg_price: float
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
