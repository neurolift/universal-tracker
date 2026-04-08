import sqlite3
import os

DB_NAME = "portfolio.db"

def create_table():
    with sqlite3.connect(DB_NAME) as conn:
        curr = conn.cursor()
        curr.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                symbol TEXT PRIMARY KEY,
                name TEXT,
                asset_type TEXT,
                price REAL,
                extra_info TEXT
            )
        ''')
        conn.commit()

def save_asset(asset_obj):
    with sqlite3.connect(DB_NAME) as conn:
        curr = conn.cursor()
        extra=getattr(asset_obj,'exchange',getattr(asset_obj,'purity',""))
        curr.execute('''
            INSERT OR REPLACE INTO assets (symbol, name, asset_type, price, extra_info)
            VALUES (?, ?, ?, ?, ?)
        ''', (asset_obj.symbol, asset_obj.name, asset_obj.__class__.__name__, asset_obj.current_price, extra))
        conn.commit()

def load_assets():
    with sqlite3.connect(DB_NAME) as conn:
        curr = conn.cursor()
        curr.execute("SELECT * FROM assets")
        return curr.fetchall()