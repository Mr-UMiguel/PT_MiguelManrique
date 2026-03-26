
def PL(amount_in:float, mid_px:float, reserve_x:int, reserve_y:int, lp_fee_bps:int, gas_usd:int) -> float:
    """
    Calculate the profit and loss of a cross-chain arbitrage opportunity given the input parameters.

    Parameters:
    - amount_in: The amount of the asset being bought/sold.
    - mid_px: The mid price of the pool.
    - reserve_x: The reserve of the first asset in the pool.
    - reserve_y: The reserve of the second asset in the pool.
    - lp_fee_bps: The liquidity provider fee in basis points.
    - gas_usd: The gas cost in USD.

    Returns:
    - The net profit or loss from the arbitrage opportunity.
    """
    fee = lp_fee_bps / 10000
    k = reserve_x * reserve_y
    amount_in_net = amount_in * (1 - fee)
    amount_out = reserve_y - (k / (reserve_x + amount_in_net)) if mid_px > 1.0 else reserve_x - (k / (reserve_y + amount_in_net))

    profit_loss = amount_out - amount_in - gas_usd
    
    return profit_loss