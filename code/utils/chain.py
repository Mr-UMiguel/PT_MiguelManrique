
from utils.publisher import Publisher

class Chain(Publisher):
    def __init__(self, chainId:str, currency_pair_mnemo:str, base_currency_reserve:int, quote_currency_reserve:int, pool_mid_px:float, lp_fee_bps:int, gas_usd:int):
        super().__init__()
        self._chainId = chainId
        self._currency_pair_mnemo = currency_pair_mnemo
        self._base_currency_reserve = base_currency_reserve
        self._quote_currency_reserve = quote_currency_reserve
        self._pool_mid_px = pool_mid_px
        self._lp_fee_bps = lp_fee_bps
        self._gas_usd = gas_usd

    def notify(self):
        super().notify(self)

    @property
    def ChainId(self):
        return self._chainId
    @property
    def CurrencyPairMnemo(self):
        return self._currency_pair_mnemo
    
    @property
    def BaseCurrencyReserve(self):
        return self._base_currency_reserve  
    @BaseCurrencyReserve.setter
    def BaseCurrencyReserve(self, value):
        self._base_currency_reserve = value
        # self.notify()  # Notify observers of the change

    @property
    def QuoteCurrencyReserve(self):
        return self._quote_currency_reserve
    @QuoteCurrencyReserve.setter
    def QuoteCurrencyReserve(self, value):
        self._quote_currency_reserve = value
        # self.notify()  # Notify observers of the change
        
    @property
    def PoolMidPx(self):
        return self._pool_mid_px
    @PoolMidPx.setter
    def PoolMidPx(self, value):
        self._pool_mid_px = value
        self.notify()  # Notify observers of the change

    @property
    def LpFeeBps(self):
        return self._lp_fee_bps
    @LpFeeBps.setter
    def LpFeeBps(self, value):
        self._lp_fee_bps = value
        # self.notify()  # Notify observers of the change

    @property
    def GasUsd(self):
        return self._gas_usd
    @GasUsd.setter
    def GasUsd(self, value):
        self._gas_usd = value
        # self.notify()  # Notify observers of the change
    