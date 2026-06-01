from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor
from src.config import settings

app = FastAPI(title="Market Data Query API")

def get_conn():
    return psycopg2.connect(settings.DATABASE_URL, cursor_factory=RealDictCursor)

@app.get("/ticks")
def query_ticks(
    symbol: str = Query(..., description="Symbol, e.g., RELIANCE"),
    exchange: str = Query("NSE", description="NSE or BSE"),
    from_time: str = Query(..., description="ISO timestamp start"),
    to_time: str = Query(..., description="ISO timestamp end")
):
    table = f"ticks_{exchange.lower()}"
    query = f"""
        SELECT * FROM market_data.{table}
        WHERE symbol = %s AND time >= %s AND time <= %s
        ORDER BY time ASC
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, (symbol, from_time, to_time))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"symbol": symbol, "exchange": exchange, "ticks": rows}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
