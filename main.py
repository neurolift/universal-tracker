from src import models
from src import fetchers
from src import database


def main():
    database.create_table()
    my_portfolio = models.Portfolio()
    amazon = models.Stock("AMAZON", "AMZN", "NASDAQ")
    gold = models.Metal("Gold", "XAU", "24K")
    my_portfolio.add_asset(amazon)
    my_portfolio.add_asset(gold)

    print("\n--- Starting Live Update ---")
    fetchers.update_all_assets(my_portfolio.assets)

    for asset in my_portfolio.assets:
        database.save_asset(asset)

    print("\n--- Current Portfolio Status ---")
    for item in my_portfolio.get_portfolio_data():
        print(f"Asset: {item['name']} | Price: {item['price']} | Type: {item['type']}")


if __name__ == "__main__":
    main()