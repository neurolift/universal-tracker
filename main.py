from src import Stock, Metal, Portfolio, create_table, save_asset, load_assets, update_all_assets

def load_portfolio():
    """Loads assets from the database into a Portfolio object."""
    portfolio = Portfolio()
    rows = load_assets()
    for row in rows:
        symbol, name, asset_type, price, extra_info = row
        if asset_type == "Stock":
            asset = Stock(name, symbol, extra_info)
        elif asset_type == "Metal":
            asset = Metal(name, symbol, extra_info)
        else:
            continue
        asset.update_price(price)
        portfolio.assets.append(asset)
    return portfolio

def main():
    create_table()
    my_portfolio = load_portfolio()
    
    while True:
        print("\n=== Universal Tracker CLI ===")
        print("1. Add Stock")
        print("2. Add Metal")
        print("3. Update Prices & View Portfolio")
        print("4. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            symbol = input("Enter Stock Symbol (e.g., AAPL): ").upper()
            name = input("Enter Company Name: ")
            exchange = input("Enter Exchange (e.g., NASDAQ): ")
            new_stock = Stock(name, symbol, exchange)
            my_portfolio.add_asset(new_stock)
            save_asset(new_stock)
            
        elif choice == '2':
            symbol = input("Enter Metal Symbol (e.g., XAU, XAG): ").upper()
            name = input("Enter Metal Name: ")
            purity = input("Enter Purity (default 24K): ") or "24K"
            new_metal = Metal(name, symbol, purity)
            my_portfolio.add_asset(new_metal)
            save_asset(new_metal)
            
        elif choice == '3':
            print("\nUpdating prices from live APIs...")
            update_all_assets(my_portfolio.assets)
            
            print("\n--- Current Portfolio Status ---")
            data = my_portfolio.get_portfolio_data()
            if not data:
                print("Portfolio is empty.")
            else:
                for item in data:
                    print(f"[{item['type']}] {item['name']} ({item['symbol']})")
                    print(f"  Price: {item['price']} | Info: {item['extra_info']}")
                    # Save updated prices back to DB
                    # We find the object in the list to save it
                    asset_obj = next(a for a in my_portfolio.assets if a.symbol == item['symbol'])
                    save_asset(asset_obj)
                    
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
