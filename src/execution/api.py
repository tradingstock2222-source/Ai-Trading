from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from src.execution.schemas import OrderRequest, Order, Position
from src.execution.order_manager import OrderManager
from src.execution.safety import SafetyManager
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Order Execution API")

order_manager: Optional[OrderManager] = None
safety_manager: Optional[SafetyManager] = None

def set_managers(om: OrderManager, sm: SafetyManager):
    global order_manager, safety_manager
    order_manager = om
    safety_manager = sm

@app.post("/orders", response_model=Order, status_code=201)
async def create_order(req: OrderRequest):
    if not order_manager:
        raise HTTPException(status_code=503, detail="Service not ready")
    order = Order(**req.dict())
    result = await order_manager.handle_new_order(order)
    if result.status == "REJECTED":
        raise HTTPException(status_code=400, detail=result.dict())
    return result

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    if not order_manager:
        raise HTTPException(503)
    order = order_manager.orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders")
async def list_orders(status: Optional[str] = Query(None)):
    if not order_manager:
        raise HTTPException(503)
    if status:
        return [o for o in order_manager.orders.values() if o.status.value == status]
    return list(order_manager.orders.values())

@app.get("/positions", response_model=list[Position])
async def get_positions():
    if not order_manager:
        raise HTTPException(503)
    with order_manager.pos_tracker.conn.cursor() as cur:
        cur.execute("SELECT symbol, exchange, net_qty, avg_price, realized_pnl, unrealized_pnl FROM positions.positions")
        rows = cur.fetchall()
    return [Position(symbol=r[0], exchange=r[1], net_qty=r[2], avg_price=r[3] or 0,
                     realized_pnl=r[4], unrealized_pnl=r[5]) for r in rows]

@app.post("/admin/kill-switch")
async def engage_kill_switch():
    if not safety_manager:
        raise HTTPException(503)
    safety_manager.engage_kill_switch()
    return {"status": "kill_switch_engaged"}

@app.post("/admin/kill-switch/reset")
async def reset_kill_switch():
    if not safety_manager:
        raise HTTPException(503)
    safety_manager.reset_kill_switch()
    return {"status": "kill_switch_reset"}

@app.get("/admin/health")
async def health():
    return {
        "status": "ok",
        "trading_allowed": safety_manager.trading_allowed() if safety_manager else False,
        "open_orders": len(order_manager.orders) if order_manager else 0
    }
