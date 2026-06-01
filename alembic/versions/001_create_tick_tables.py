"""create tick tables

Revision ID: 001
Revises: None
Create Date: 2026-06-01

"""
from alembic import op

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        CREATE SCHEMA IF NOT EXISTS market_data;

        CREATE TABLE market_data.ticks_nse (
            time        TIMESTAMPTZ NOT NULL,
            symbol      VARCHAR(20) NOT NULL,
            last_price  DOUBLE PRECISION NOT NULL,
            volume      BIGINT NOT NULL,
            bid         DOUBLE PRECISION,
            ask         DOUBLE PRECISION,
            bid_qty     BIGINT,
            ask_qty     BIGINT,
            exchange    VARCHAR(5) DEFAULT 'NSE',
            ingested_at TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (time, symbol)
        );

        SELECT create_hypertable('market_data.ticks_nse', 'time', if_not_exists => TRUE);
        CREATE INDEX idx_ticks_nse_symbol_time ON market_data.ticks_nse (symbol, time DESC);

        CREATE TABLE market_data.ticks_bse (LIKE market_data.ticks_nse INCLUDING ALL);
        SELECT create_hypertable('market_data.ticks_bse', 'time', if_not_exists => TRUE);
        CREATE INDEX idx_ticks_bse_symbol_time ON market_data.ticks_bse (symbol, time DESC);
    """)

def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS market_data.ticks_bse CASCADE;
        DROP TABLE IF EXISTS market_data.ticks_nse CASCADE;
        DROP SCHEMA IF EXISTS market_data CASCADE;
    """)
