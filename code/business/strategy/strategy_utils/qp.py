from typing import Tuple
from scipy.optimize import minimize_scalar

from .pl import PL



def optimize(mid_px:float, reserve_x:int, reserve_y:int, lp_fee_bps:int, gas_usd:int, amount_in_bounds: Tuple[float, float]) -> Tuple[float, float]:
    """
    Optimize the amount to buy/sell for maximizing profit in a cross-chain arbitrage opportunity.

    Parameters:
    - mid_px: The mid price of the pool.
    - reserve_x: The reserve of the first asset in the pool.
    - reserve_y: The reserve of the second asset in the pool.
    - lp_fee_bps: The liquidity provider fee in basis points.
    - gas_usd: The gas cost in USD.

    Returns:
    - A tuple containing the optimal amount to buy/sell and the corresponding profit/loss.
    """
    result = minimize_scalar(lambda x: -PL(x, mid_px, reserve_x, reserve_y, lp_fee_bps, gas_usd), bounds=amount_in_bounds, method='bounded')
    
    optimal_amount = result.x
    optimal_pl = -result.fun
    
    return optimal_amount, optimal_pl