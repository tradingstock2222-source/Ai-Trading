import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ['time', 'symbol', 'last_price', 'volume', 'exchange']

def validate_tick(tick: dict) -> bool:
    for field in REQUIRED_FIELDS:
        if field not in tick:
            logger.warning(f"Missing field: {field}")
            return False

    try:
        ts = datetime.fromisoformat(tick['time'])
        if ts > datetime.now(timezone.utc):
            logger.warning(f"Future timestamp: {tick['time']}")
            return False
    except Exception as e:
        logger.warning(f"Bad timestamp: {tick['time']} {e}")
        return False

    if tick['last_price'] <= 0:
        logger.warning(f"Non-positive price: {tick['last_price']}")
        return False

    if tick['volume'] < 0:
        logger.warning(f"Negative volume: {tick['volume']}")
        return False

    if tick['exchange'] not in ('NSE', 'BSE'):
        logger.warning(f"Unknown exchange: {tick['exchange']}")
        return False

    return True
