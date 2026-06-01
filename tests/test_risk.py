from src.risk.basic_risk import parametric_var

def test_var_calculation():
    prices = [100, 102, 101, 99, 98, 97, 103, 104]
    var = parametric_var(prices, confidence=0.95)
    assert 2.0 < var < 8.0
