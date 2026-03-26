from utils.observer import Observer 
from utils.chain import Chain
from .strategy_utils.riskcontrol import RISK_CONTROL_CONFIG
from .strategy_utils.qp import optimize


class CrossChainArb(Observer):
    RISK_CONTROL_SETTINGS = RISK_CONTROL_CONFIG
    ## JSON LABELS
    CHAIN = 'chain'
    COPW_RESERVE = 'copw_reserve'
    TCOPW_RESERVE = 'tcopw_reserve'
    POOL_MID_PX = 'pool_mid_px'
    LP_FEE_BPS = 'lp_fee_bps'
    GAS_USD = 'gas_usd'
    ## OPTIMIZATION BOUNDARIES
    AMOUNT_IN_BOUNDS = (10000.0,100000.0)

    ## Strategy in-memory variables
    __last_px_mid = None

    def __init__(self, config:dict=None):
        super().__init__()

    def update(self,message:Chain):
        chain = message.ChainId
        mid_px = message.PoolMidPx
        reserve_x = message.BaseCurrencyReserve
        reserve_y = message.QuoteCurrencyReserve
        lp_fee_bps = message.LpFeeBps
        gas_usd = message.GasUsd
        side = 'buy' if mid_px > 1.0 else 'sell'

        optimal_amount, optimal_pl = optimize(mid_px, reserve_x, reserve_y, lp_fee_bps, gas_usd, amount_in_bounds=self.AMOUNT_IN_BOUNDS)
        risk_control = self.risk_control(mid_px, optimal_amount, optimal_pl)
        self.__last_px_mid = mid_px

        if risk_control == True:
            print(f"Signal: {side.upper()} {optimal_amount:.2f} with expected P/L: {optimal_pl:.2f}\n")

    
    def risk_control(self, mid_px:float, optimal_amount:float, optimal_pl:float) -> bool:
        # Implement risk control logic based on the RISK_CONTROL_SETTINGS
        if optimal_pl < self.RISK_CONTROL_SETTINGS['min_profit_usd']:
            print("Risk control triggered: Profit below minimum threshold. No trade executed.")
            return False
        if optimal_amount < self.RISK_CONTROL_SETTINGS['min_size'] or optimal_amount > self.RISK_CONTROL_SETTINGS['max_size']:
            print("Risk control triggered: Trade size out of bounds. No trade executed.")
            return False 
        if (self.__last_px_mid is not None and abs((self.__last_px_mid - mid_px) / self.__last_px_mid)  > self.RISK_CONTROL_SETTINGS['max_mid_px_deviation_bps'] / 10000):
            print("Risk control triggered: Mid price deviation too high. No trade executed.")
            return False
        # Additional risk control checks can be implemented here
        return True
    
    def kill_switch(self):
        # Implement logic to deactivate the strategy if certain conditions are met
        print("Kill switch activated. Deactivating strategy.")
    
    ## Pre trade checks
    def WalletReserveOracle(self):
        """Watch if we have enough reserves must be implemented with risk controls"""
        
    ## Post-trade check    
    def DropCopy(self):
        """Supervise the order execution"""

    ## Reconociliation
    def UpdateWalletReserve(self):
        """If some profit or loss is incurred then update the reserves"""