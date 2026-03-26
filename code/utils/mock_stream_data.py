from .chain import Chain

import asyncio
import json
import os 

## constant path settings
ROOTH_PATH  = os.getcwd()
SOURCE_PATH = os.path.join(ROOTH_PATH, './source')
FILE_PATH   = os.path.join(SOURCE_PATH, 'mock_lp_mkt_data.json')

## JSON LABELS
CHAIN = 'chain'
COPW_RESERVE = 'copw_reserve'
TCOPW_RESERVE = 'tcopw_reserve'
POOL_MID_PX = 'pool_mid_px'
LP_FEE_BPS = 'lp_fee_bps'
GAS_USD = 'gas_usd'

async def stream_chain_data(chain: Chain):
    """Simulates streaming data updates to the Chain observer by reading from a JSON file."""
    print(f"Starting to stream data for Chain ID: {chain.ChainId}")

    while True:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)

        for entry in data:
            reserve_x = entry[COPW_RESERVE]
            reserve_y = entry[TCOPW_RESERVE]
            lp_fee_bps = entry[LP_FEE_BPS]
            gas_usd = entry[GAS_USD]
            mid_px = entry[POOL_MID_PX]

            chain.BaseCurrencyReserve = reserve_x
            chain.QuoteCurrencyReserve = reserve_y 
            chain.LpFeeBps = lp_fee_bps
            chain.GasUsd = gas_usd
            chain.PoolMidPx = mid_px 
            print(f"Updating Chain with new mid price: {mid_px}")
            await asyncio.sleep(5)  # Simulate a delay between updates