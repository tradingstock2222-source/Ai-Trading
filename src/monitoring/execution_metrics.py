from prometheus_client import Counter, Gauge, Histogram

orders_submitted = Counter(
    'orders_submitted_total',
    'Total orders submitted',
    ['side', 'order_type']
)

orders_completed = Counter(
    'orders_completed_total',
    'Orders reaching terminal state',
    ['side', 'status']
)

orders_rejected = Counter(
    'orders_rejected_total',
    'Orders rejected by pre-trade risk',
    ['reason']
)

order_latency = Histogram(
    'order_latency_seconds',
    'Latency from order creation to terminal state',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

open_orders = Gauge(
    'open_orders',
    'Number of currently open orders'
)

position_value = Gauge(
    'position_value',
    'Current position market value',
    ['symbol']
)

circuit_breaker_status = Gauge(
    'circuit_breaker_status',
    'Circuit breaker status (1 = tripped, 0 = normal)'
)

kill_switch_status = Gauge(
    'kill_switch_status',
    'Kill switch status (1 = engaged, 0 = active)'
)

broker_heartbeat_age = Gauge(
    'broker_heartbeat_age_seconds',
    'Seconds since last broker heartbeat'
)
