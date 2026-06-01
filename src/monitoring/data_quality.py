from prometheus_client import Counter, start_http_server

ticks_ingested = Counter('ticks_ingested_total', 'Total ticks received from Kafka')
ticks_validated = Counter('ticks_validated_total', 'Ticks that passed validation')
validation_failures = Counter('validation_failures_total', 'Ticks that failed validation')

def start_monitoring_server(port=8001):
    start_http_server(port)
