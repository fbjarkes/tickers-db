
import argparse
import sqlite3
import logging
import asyncio
import nest_asyncio
from ib_async import Contract, IB, StartupFetch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def build_sectors_mapping(symbols_dict):
    """
    Given a dictionary with symbol as key and a tuple (industry, sector, sub_sector) as value,
    build a mapping that returns the number of symbols in each ib_industry, ib_sector, ib_sub_sector respectively.
    """
    sector_mapping = {}

    for symbol, (industry, sector, sub_sector) in symbols_dict.items():
        if industry not in sector_mapping:
            sector_mapping[industry] = {'count': 0}
        sector_mapping[industry]['count'] += 1

        if sector:
            if sector not in sector_mapping:
                sector_mapping[sector] = {'count': 0}
            sector_mapping[sector]['count'] += 1

        if sub_sector:
            if sub_sector not in sector_mapping:
                sector_mapping[sub_sector] = {'count': 0}
            sector_mapping[sub_sector]['count'] += 1

    return sector_mapping

def get_positions_json():
    return {
        'AAL': {'qty': 10, 'pnl': -10.2, 'value': 200},
        'ABAT': {'qty': 5, 'pnl': 50.0, 'value': 1500},
        'AAPL': {'qty': 3, 'pnl': 20.5, 'value': 900},
        'AAOI': {'qty': 4, 'pnl': 30.0, 'value': 800},
        'AAON': {'qty': 6, 'pnl': 15.0, 'value': 900}
    }

def get_sector(sym, cursor):    
    cursor.execute("SELECT ib_industry, ib_sector, ib_sub_sector FROM tickers WHERE symbol=?", (sym,))
    result = cursor.fetchone()

    if result:
        sector, category, sub_category = result
    else:
        sector, category, sub_category = '', '', ''
    
    return sector, category, sub_category

def main(args):
    try:
        conn = sqlite3.connect(args.db)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return
    
    positions = get_positions_json()
    # Create a dictionary with symbol as key and a tuple (industry, sector, sub_sector) as value for each symbol in positions, use get_sector() 
    symbols_dict = {symbol: get_sector(symbol, cursor) for symbol in positions.keys()}
    sector_mapping = build_sectors_mapping(symbols_dict)

    # pretty print
    for key, value in sector_mapping.items():
        print(f"{key}: {value}")

    # ib = IB()

    # if not ib.connect(host=args.host, port=args.port, fetchFields=StartupFetch.POSITIONS):
    #     logging.error("Error connecting to IB")
    #     conn.close()
    #     return



    #ib.disconnect()
    conn.close()
    
    
if __name__ == "__main__":
    import sys    
    sys.argv = ['ib_sectors.py', '--host', '192.168.1.51', '--port', '7496', '--db', 'db/sqlite/tickers.sqlite']
    
    parser = argparse.ArgumentParser(description='Get industry sector information.')
    parser.add_argument('--host', type=str, required=True, help='Host IP address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--db', type=str, required=True, help='Database file path')
    args = parser.parse_args()
    main(args)
