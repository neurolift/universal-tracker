import requests
import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GOLD_API_KEY")

def get_stock_data(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        raw_data = stock.info
        if not raw_data:
            return None
            
        clean_data = {
            "symbol": raw_data.get("symbol"),
            "name": raw_data.get("longName"),
            "price": raw_data.get("currentPrice") or raw_data.get("regularMarketPrice"),
            "currency": raw_data.get("currency"),
            "change": raw_data.get("regularMarketChangePercent")
        }
        return clean_data
    except Exception as e:
        print(f"Error fetching stock data for {ticker_symbol}: {e}")
        return None


def get_metal_data(symbol="XAU"):
    url = f"https://www.goldapi.io/api/{symbol}/USD"
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        return {
            "symbol": result.get("metal"),
            "name": f"{result.get('metal')} (24k)",
            "price": result.get('price_gram_24k'), 
            "currency": result.get('currency'),
            "change": result.get("chp")
        }
    except Exception as e:
        print(f"Error fetching metal data: {e}")
        return None


def update_all_assets(asset_list):
    """The Master Fetcher: Loops through objects and updates them."""
    for asset in asset_list:
        try:
            asset_type = asset.__class__.__name__
            
            if asset_type == "Stock":
                data = get_stock_data(asset.symbol)
            elif asset_type == "Metal":
                data = get_metal_data(asset.symbol)
            else:
                data = None

            if data and data.get('price'):
                asset.update_price(data['price'])
                print(f"Updated {asset.name} to {data['price']} {data.get('currency', 'USD')}")
            else:
                print(f"Warning: No valid data for {asset.symbol}")
                
        except Exception as e:
            print(f"Could not update {asset.symbol}: {e}")

if __name__ == "__main__":
    # Test cases
    print("Testing fetchers...")
    print(get_stock_data("AMZN"))
    print(get_metal_data("XAU"))
