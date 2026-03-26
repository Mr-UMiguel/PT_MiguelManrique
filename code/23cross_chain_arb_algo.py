
from business.strategy.crossChainArb import CrossChainArb
from utils.chain import Chain
from utils.mock_stream_data import stream_chain_data

import asyncio

async def main():
    # Simulate receiving a message from the Chain observer
    base_sample_message = {
        'ChainId': 'chain_1',
        'PoolMidPx': 1.05,
        'BaseCurrencyReserve': 50000.0,
        'QuoteCurrencyReserve': 48000.0,
        'LpFeeBps': 30,
        'GasUsd': 10.0
    }

    #Mock chain behavior
    mock_chain = Chain(
        chainId=base_sample_message['ChainId'],
        currency_pair_mnemo='ETH/USD',
        base_currency_reserve=base_sample_message['BaseCurrencyReserve'],
        quote_currency_reserve=base_sample_message['QuoteCurrencyReserve'],
        pool_mid_px=base_sample_message['PoolMidPx'],
        lp_fee_bps=base_sample_message['LpFeeBps'],
        gas_usd=base_sample_message['GasUsd']
    )

    # Initialize the CrossChainArb strategy
    cross_chain_arb_strategy = CrossChainArb(config={})
    
    mock_chain.attach(cross_chain_arb_strategy)
    await stream_chain_data(mock_chain)
    
if __name__ == "__main__":
    try:
        print("Starting Cross-Chain Arbitrage Strategy...\n")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting.")
    