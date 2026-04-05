class Asset:
    def __init__(self,name,symbol):
        self.name=name
        self.symbol=symbol
        self.current_price=0.0
    def update_price(self,new_price):
        self.current_price=new_price
    def to_dict(self):
        return {"name":self.name,
                "symbol":self.symbol,
                "price":self.current_price,
                "type":self.__class__.__name__}

class Stock(Asset):
    def __init__(self,name,symbol,exchange):
        super().__init__(name,symbol)
        self.exchange=exchange


class Metal(Asset):
    def __init__(self,name,symbol,purity="24K"):
        super().__init__(name,symbol)
        self.purity=purity
    def calculate_per_tola(self,usd_to_npr):
        return f"Price per Tola: {(self.current_price*usd_to_npr)/2.66}"

class Portfolio:
    def __init__(self):
        self.assets=[]
    def add_asset(self,asset_obj):
        '''To avoid any asset duplicates by checking if it is already in the list or not '''
        exists = any(a.symbol == asset_obj.symbol for a in self.assets)
        if not exists:
            self.assets.append(asset_obj)
            print(f"Added {asset_obj.name} ({asset_obj.symbol}) to portfolio.")
        else:
            print(f"Asset {asset_obj.symbol} is already in the portfolio")
    def update_all_prices(self,fetcher_function):
        '''This loops thorugh every assest and updtaes its price using your fetching logic'''
        for asset in self.assets:
            new_price_data=fetcher_function(asset.symbol)
            if new_price_data:
                asset.update_price(new_price_data['price'])
    def get_portfolio_data(self):
        return [asset.to_dict() for asset in self.assets]