from src import models
from src import fetchers
from src import database
import json

def load_data_set():
    try:
        with open("sp500.json","r") as f:
            return json.load(f)["stocks"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def main():
    database.create_table()
    my_portfolio=models.Portfolio()
    gold=models.Metal("Gold","XAU","24K")
    stocks=load_data_set()
   
    for stock in stocks:
        stock_asset=models.Stock(stock["name"],stock["symbol"],stock.get("exchange"))
        my_portfolio.add_asset(stock_asset)

    my_portfolio.add_asset(gold)

    print("\n--- Starting Live Update ---")

    fetchers.update_all_assets(my_portfolio.assets)

    for asset in my_portfolio.assets:
        database.save_asset(asset)

    print("\n--- Current Portfolio Status ---")
    for item in my_portfolio.get_portfolio_data():

        print(f"Asset: {item['name']} | Price: {item['price']} | Type: {item["type"]}")
if __name__=="__main__":
    main()