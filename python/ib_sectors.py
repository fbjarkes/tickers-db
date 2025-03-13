import argparse
import sqlite3
import logging
from ib_async import Contract, IB, StartupFetch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BATCH_LIMIT = 1000

def get_industry_sector(ib, symbol, exchange="SMART", currency="USD"):
    contract = Contract(symbol=symbol, secType="STK", exchange=exchange, currency=currency)
    contract_details = ib.reqContractDetails(contract)

    if contract_details:
        contract_detail = contract_details[0]  # taking the first result
        return contract_detail.industry, contract_detail.category, contract_detail.subcategory
    logging.warning(f"Could not retrieve contract details for {symbol}.")
    return None, None, None

def process_updates(cursor, updates):
    cursor.executemany("""
        UPDATE tickers
        SET ib_industry = ?, ib_sector = ?, ib_sub_sector = ?
        WHERE symbol = ?
    """, updates)


def main(args):
    try:
        conn = sqlite3.connect(args.db)
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return

    cursor = conn.cursor()
    ib = IB()

    if not ib.connect(host=args.host, port=args.port, fetchFields=StartupFetch.POSITIONS):
        logging.error("Error connecting to IB")
        conn.close()
        return

    cursor.execute("SELECT symbol FROM tickers LIMIT 100")
    rows = cursor.fetchall()

    updates = []
    for row in rows:
        symbol = row[0]
        logging.info(f"Processing symbol: {symbol}")
        industry, sector, sub_category = get_industry_sector(ib, symbol)
        if industry and sector and sub_category:
            logging.info(f"Updating symbol: {symbol} with industry: {industry}, sector: {sector}, sub_category: {sub_category}")
            updates.append((industry, sector, sub_category, symbol))

        if len(updates) >= BATCH_LIMIT:
            process_updates(cursor, updates)
            updates = []

    if updates:
        process_updates(cursor, updates)

    ib.disconnect()
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
