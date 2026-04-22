from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BigONEExchangeData(ExchangeData):
    def __init__(self):
        super().__init__()
        self.exchange_name = "BIGONE___SPOT"
        self.rest_url = "https://big.one/api/v3"
        self.wss_url = "wss://big.one/ws/v2"
        self.rest_paths = {}
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "min1",
            "5m": "min5",
            "15m": "min15",
            "30m": "min30",
            "1h": "hour1",
            "4h": "hour4",
            "12h": "hour12",
            "1d": "day1",
            "1w": "week1",
            "1M": "month1",
        }
        self.legal_currency = ["USDT", "USD", "BTC", "ETH", "EUR"]

    def get_symbol(self, symbol):
        s = symbol.upper().replace("/", "-").replace("_", "-")
        return s

    def get_period(self, period):
        return self.kline_periods.get(period, period)

    def get_rest_path(self, request_type, **kwargs):
        path = self.rest_paths.get(request_type)
        if path is None:
            raise ValueError(f"Unknown rest path: {request_type}")
        return path

    def get_wss_path(self, channel_type, symbol=None, **kwargs):
        path = self.wss_paths.get(channel_type, "")
        if symbol and "{symbol}" in str(path):
            path = str(path).replace("{symbol}", self.get_symbol(symbol))
        return path


class BigONEExchangeDataSpot(BigONEExchangeData):
    def __init__(self):
        super().__init__()
        self.asset_type = "spot"
        self.exchange_name = "BIGONE___SPOT"
        self.rest_url = "https://big.one/api/v3"
        self.wss_url = "wss://big.one/ws/v2"
        self.rest_paths = {
            "get_server_time": "GET /ping",
            "get_exchange_info": "GET /asset_pairs",
            "get_tick": "GET /asset_pairs/{symbol}/ticker",
            "get_tick_all": "GET /asset_pairs/tickers",
            "get_depth": "GET /asset_pairs/{symbol}/depth",
            "get_trades": "GET /asset_pairs/{symbol}/trades",
            "get_kline": "GET /asset_pairs/{symbol}/candles",
            "make_order": "POST /viewer/orders",
            "cancel_order": "POST /viewer/orders/{order_id}/cancel",
            "cancel_all_orders": "POST /viewer/orders/cancel",
            "get_open_orders": "GET /viewer/orders",
            "query_order": "GET /viewer/orders/{order_id}",
            "get_deals": "GET /viewer/trades",
            "get_balance": "GET /viewer/accounts",
            "get_account": "GET /viewer/accounts",
        }


BigONESpotExchangeData = BigONEExchangeDataSpot

__all__ = ["BigONEExchangeData", "BigONEExchangeDataSpot", "BigONESpotExchangeData"]
