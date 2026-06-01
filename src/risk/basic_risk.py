import numpy as np
from scipy.stats import norm

def parametric_var(prices: list, confidence: float = 0.95, holding_period: int = 1) -> float:
    """
    Returns 1-day VaR as a positive loss amount.
    prices: list of closing prices (most recent last).
    """
    if len(prices) < 2:
        raise ValueError("At least 2 prices required")
    returns = np.diff(prices) / prices[:-1]
    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)
    z = norm.ppf(1 - confidence)
    var = -(mu + z * sigma) * np.sqrt(holding_period) * prices[-1]
    return abs(var)
