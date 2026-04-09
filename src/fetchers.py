import requests
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GOLD_API_KEY")


def _get_gold_price_from_yfinance():
    """Fallback source for gold spot/futures when GoldAPI is unavailable."""
    ticker = yf.Ticker("GC=F")
    raw_data = ticker.info
    price = raw_data.get("currentPrice") or raw_data.get("regularMarketPrice")

    if price is None:
        return None

    return {
        "symbol": "XAU",
        "name": "Gold",
        "price": price,
        "currency": raw_data.get("currency", "USD"),
        "change": raw_data.get("regularMarketChangePercent"),
    }

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


def get_metal_data(symbol="XAU"):

    if not api_key:
        return _get_gold_price_from_yfinance()

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
            print("GoldAPI request failed, falling back to yfinance:", str(e))
            return _get_gold_price_from_yfinance()

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