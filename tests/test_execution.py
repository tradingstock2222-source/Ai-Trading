import pytest
from fastapi.testclient import TestClient
from src.execution.api import app
from src.execution.schemas import OrderRequest, OrderType, Side

@pytest.fixture
def client():
    return TestClient(app)

def test_create_market_buy_order(client):
    req = OrderRequest(
        symbol="RELIANCE",
        exchange="NSE",
        order_type=OrderType.MARKET,
        side=Side.BUY,
        quantity=100
    )
    response = client.post("/orders", json=req.dict())
    assert response.status_code == 201
    data = response.json()
    assert data["symbol"] == "RELIANCE"
    assert data["side"] == "BUY"
    assert data["status"] in ("VALIDATED", "ROUTED", "FILLED", "PARTIAL")

def test_create_zero_quantity_order(client):
    req = OrderRequest(
        symbol="TCS",
        exchange="NSE",
        order_type=OrderType.LIMIT,
        side=Side.SELL,
        quantity=0,
        price=3500.0
    )
    response = client.post("/orders", json=req.dict())
    assert response.status_code == 400

def test_get_order_not_found(client):
    response = client.get("/orders/nonexistent-id")
    assert response.status_code == 404

def test_health_endpoint(client):
    response = client.get("/admin/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_kill_switch_engage_reset(client):
    r = client.post("/admin/kill-switch")
    assert r.status_code == 200
    assert r.json()["status"] == "kill_switch_engaged"
    req = OrderRequest(symbol="INFY", exchange="NSE", order_type=OrderType.MARKET, side=Side.BUY, quantity=50)
    r2 = client.post("/orders", json=req.dict())
    assert r2.status_code == 400
    r3 = client.post("/admin/kill-switch/reset")
    assert r3.status_code == 200
    r4 = client.post("/orders", json=req.dict())
    assert r4.status_code == 201

def test_full_lifecycle(client):
    req = OrderRequest(symbol="HDFCBANK", exchange="NSE", order_type=OrderType.MARKET, side=Side.BUY, quantity=200)
    resp = client.post("/orders", json=req.dict())
    assert resp.status_code == 201
    order_id = resp.json()["order_id"]

    resp2 = client.get(f"/orders/{order_id}")
    assert resp2.status_code == 200
    assert resp2.json()["order_id"] == order_id

    resp3 = client.get("/orders")
    assert resp3.status_code == 200
    orders = resp3.json()
    assert any(o["order_id"] == order_id for o in orders)
