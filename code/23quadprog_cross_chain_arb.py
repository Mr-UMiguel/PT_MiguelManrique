
## Data and system handling libraries
from typing import Tuple, List
import json
import os

## optimization library
from scipy.optimize import minimize_scalar

## constant path settings
ROOTH_PATH  = os.getcwd()
SOURCE_PATH = os.path.join(ROOTH_PATH, './source')
FILE_PATH   = os.path.join(SOURCE_PATH, 'cross_chain_arb.json')


## OPTIMIZATION BOUNDARIES
AMOUNT_IN_BOUNDS = (10000.0,100000.0)

## JSON LABELS
CHAIN = 'chain'
COPW_RESERVE = 'copw_reserve'
TCOPW_RESERVE = 'tcopw_reserve'
POOL_MID_PX = 'pool_mid_px'
LP_FEE_BPS = 'lp_fee_bps'
GAS_USD = 'gas_usd'

def LoadData(file_path: str) -> List[dict]:
    """
    Load data from a JSON file.

    Parameters:
    - file_path: The path to the JSON file.

    Returns:
    - A list of data entries loaded from the JSON file.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


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

def optimize(mid_px:float, reserve_x:int, reserve_y:int, lp_fee_bps:int, gas_usd:int) -> Tuple[float, float]:
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
    result = minimize_scalar(lambda x: -PL(x, mid_px, reserve_x, reserve_y, lp_fee_bps, gas_usd), bounds=AMOUNT_IN_BOUNDS, method='bounded')
    
    optimal_amount = result.x
    optimal_pl = -result.fun
    
    return optimal_amount, optimal_pl

def main():
    data = LoadData(FILE_PATH)   
    for entry in data:
        mid_px = entry[POOL_MID_PX]
        reserve_x = entry[COPW_RESERVE]
        reserve_y = entry[TCOPW_RESERVE]
        lp_fee_bps = entry[LP_FEE_BPS]
        gas_usd = entry[GAS_USD]

        optimal_amount, optimal_pl = optimize(mid_px, reserve_x, reserve_y, lp_fee_bps, gas_usd)
        
        print(f"Chain: {entry[CHAIN]}, Optimal Amount: {optimal_amount:.2f}, Optimal P/L: {optimal_pl:.2f}")

if __name__ == "__main__":
    main()