import numpy as np
from src.risk.basic_risk import parametric_var

# Generate synthetic price series
prices = np.cumsum(np.random.randn(252) * 2 + 100)

# Calculate 1-day 95% VaR
var = parametric_var(prices, confidence=0.95)
print(f'1-day 95% VaR: {var:.2f}')
