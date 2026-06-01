from src.data_validation.validator import validate_tick

def test_valid_tick():
    tick = {
        'time': '2026-06-01T12:00:00+00:00',
        'symbol': 'RELIANCE',
        'last_price': 2500.0,
        'volume': 1000,
        'exchange': 'NSE'
    }
    assert validate_tick(tick) == True

def test_missing_field():
    tick = {'time': '2026-06-01T12:00:00+00:00', 'symbol': 'RELIANCE'}
    assert validate_tick(tick) == False

def test_future_timestamp():
    tick = {
        'time': '2099-01-01T12:00:00+00:00',
        'symbol': 'RELIANCE',
        'last_price': 2500.0,
        'volume': 1000,
        'exchange': 'NSE'
    }
    assert validate_tick(tick) == False

def test_negative_price():
    tick = {
        'time': '2026-06-01T12:00:00+00:00',
        'symbol': 'RELIANCE',
        'last_price': -10.0,
        'volume': 1000,
        'exchange': 'NSE'
    }
    assert validate_tick(tick) == False

def test_negative_volume():
    tick = {
        'time': '2026-06-01T12:00:00+00:00',
        'symbol': 'RELIANCE',
        'last_price': 2500.0,
        'volume': -5,
        'exchange': 'NSE'
    }
    assert validate_tick(tick) == False
