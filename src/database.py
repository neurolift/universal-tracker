import sqlite3
DB_NAME="portolio.db"
def create_table():
    conn=sqlite3.connect(DB_NAME)
    curr=conn.cursor()
    curr.execute('''create table if not exists assets(
    symbol text primary key,
                 name text,
                 asset_type text,
                 price real,
                 extra_info text)''')
    conn.commit()
    conn.close()
def save_asset(asset_obj):
    conn=sqlite3.connect(DB_NAME)
    curr=conn.cursor()
    extra=getattr(asset_obj,'exchange',getattr(asset_obj,'purity',""))
    curr.execute('''
        INSERT OR REPLACE INTO assets (symbol, name, asset_type, price, extra_info)
        VALUES (?, ?, ?, ?, ?)
    ''', (asset_obj.symbol, asset_obj.name, asset_obj.__class__.__name__, asset_obj.current_price, extra))
    conn.commit()
    conn.close()

def load_assets():
    conn=sqlite3.connect(DB_NAME)
    curr=conn.cursor()
    curr.execute("SELECT * FROM assets")
    rows=curr.fetchall()
    conn.close()
    return rows