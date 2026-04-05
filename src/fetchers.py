import requests
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GOLD_API_KEY")

def get_stock_data(ticker_symbol):
    stock=yf.Ticker(ticker_symbol)
    raw_data=stock.info
    clean_data = {
    "symbol": raw_data.get("symbol"),
    "name": raw_data.get("longName"),
    "price": raw_data.get("currentPrice"),
    "currency": raw_data.get("currency"),
    "change": raw_data.get("regularMarketChangePercent")
}
    return clean_data
print(get_stock_data("AMZN"))


def get_metal_data(symbol="XAU"):

    url = f"https://www.goldapi.io/api/{symbol}/USD"
    
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result=response.json()
        return {
            "symbol": result.get("metal"),
            "name": "Gold (24k)",
            "price": result['price_gram_24k'], 
            "currency": result['currency'],
            "change": result.get("chp")
                }
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

print(get_metal_data())

def update_all_assets(asset_list):
    """The Master Fetcher: Loops through objects and updates them."""
    for asset in asset_list:
        try:
            # We check class names as strings to avoid importing models.py
            asset_type = asset.__class__.__name__
            
            if asset_type == "Stock":
                data = get_stock_data(asset.symbol)
            elif asset_type == "Metal":
                data = get_metal_data(asset.symbol)
            else:
                data = None

            if data:
                asset.update_price(data['price'])
                print(f"Successfully updated {asset.name} to {data['price']} {data['currency']}")
                
        except Exception as e:
            print(f"Could not update {asset.symbol}: {e}")