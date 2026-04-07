class Asset:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.current_price = 0.0

    def update_price(self, new_price):
        self.current_price = new_price

    def to_dict(self):
        return {
            "name": self.name,
            "symbol": self.symbol,
            "price": self.current_price,
            "type": self.__class__.__name__,
            "extra_info": self.get_extra_info()
        }

    def get_extra_info(self):
        return ""

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.symbol}, {self.current_price})>"


class Stock(Asset):
    def __init__(self, name, symbol, exchange):
        super().__init__(name, symbol)
        self.exchange = exchange

    def get_extra_info(self):
        return self.exchange


class Metal(Asset):
    def __init__(self, name, symbol, purity="24K"):
        super().__init__(name, symbol)
        self.purity = purity

    def get_extra_info(self):
        return self.purity

    def calculate_per_tola(self, usd_to_npr):
        return (self.current_price * usd_to_npr) / 2.66


class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset_obj):
        """Adds an asset to the portfolio, avoiding duplicates."""
        exists = any(a.symbol == asset_obj.symbol for a in self.assets)
        if not exists:
            self.assets.append(asset_obj)
            print(f"Added {asset_obj.name} ({asset_obj.symbol}) to portfolio.")
        else:
            print(f"Asset {asset_obj.symbol} is already in the portfolio")

    def update_all_prices(self, fetcher_function):
        """Updates all prices in the portfolio using a fetcher logic."""
        for asset in self.assets:
            new_price_data = fetcher_function(asset.symbol)
            if new_price_data:
                asset.update_price(new_price_data['price'])

    def get_portfolio_data(self):
        return [asset.to_dict() for asset in self.assets]