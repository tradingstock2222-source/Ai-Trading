"""create order execution tables

Revision ID: 002
Revises: 001
Create Date: 2026-06-01

"""
from alembic import op

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        CREATE SCHEMA IF NOT EXISTS orders;
        CREATE SCHEMA IF NOT EXISTS positions;

        -- Orders
        CREATE TABLE orders.orders (
            order_id        UUID PRIMARY KEY,
            symbol          VARCHAR(20) NOT NULL,
            exchange        VARCHAR(5) NOT NULL,
            order_type      VARCHAR(10) NOT NULL,
            side            VARCHAR(4) NOT NULL,
            quantity        BIGINT NOT NULL,
            price           DOUBLE PRECISION,
            status          VARCHAR(20) NOT NULL DEFAULT 'PENDING',
            filled_qty      BIGINT DEFAULT 0,
            avg_price       DOUBLE PRECISION,
            created_at      TIMESTAMPTZ DEFAULT NOW(),
            updated_at      TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE INDEX idx_orders_symbol_status ON orders.orders (symbol, status);

        -- Order Events (Audit Trail)
        CREATE TABLE orders.order_events (
            event_id        BIGSERIAL PRIMARY KEY,
            order_id        UUID NOT NULL REFERENCES orders.orders(order_id),
            event_type      VARCHAR(30) NOT NULL,
            event_data      JSONB,
            created_at      TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE INDEX idx_events_order ON orders.order_events (order_id);

        -- Executions (Fills)
        CREATE TABLE orders.executions (
            exec_id         UUID PRIMARY KEY,
            order_id        UUID NOT NULL REFERENCES orders.orders(order_id),
            symbol          VARCHAR(20) NOT NULL,
            exchange        VARCHAR(5) NOT NULL,
            side            VARCHAR(4) NOT NULL,
            quantity        BIGINT NOT NULL,
            price           DOUBLE PRECISION NOT NULL,
            commission      DOUBLE PRECISION DEFAULT 0,
            exec_time       TIMESTAMPTZ NOT NULL,
            created_at      TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE INDEX idx_exec_order ON orders.executions (order_id);
        CREATE INDEX idx_exec_symbol_time ON orders.executions (symbol, exec_time DESC);

        -- Positions
        CREATE TABLE positions.positions (
            symbol          VARCHAR(20) NOT NULL,
            exchange        VARCHAR(5) NOT NULL,
            net_qty         BIGINT NOT NULL DEFAULT 0,
            avg_price       DOUBLE PRECISION,
            realized_pnl    DOUBLE PRECISION DEFAULT 0,
            unrealized_pnl  DOUBLE PRECISION DEFAULT 0,
            updated_at      TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (symbol, exchange)
        );
    """)

def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS positions.positions CASCADE;
        DROP TABLE IF EXISTS orders.executions CASCADE;
        DROP TABLE IF EXISTS orders.order_events CASCADE;
        DROP TABLE IF EXISTS orders.orders CASCADE;
        DROP SCHEMA IF EXISTS positions CASCADE;
        DROP SCHEMA IF EXISTS orders CASCADE;
    """)
