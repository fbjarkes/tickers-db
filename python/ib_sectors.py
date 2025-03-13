import argparse
import sqlite3
import logging
from ib_async import Contract, IB, StartupFetch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_industry_sector(ib, symbol, exchange="SMART", currency="USD"):
    contract = Contract(symbol=symbol, secType="STK", exchange=exchange, currency=currency)
    contract_details = ib.reqContractDetails(contract)

    if contract_details:
        contract_detail = contract_details[0]  # taking the first result
        return contract_detail.industry, contract_detail.category, contract_detail.subcategory
    logging.warning(f"Could not retrieve contract details for {symbol}.")
    return None, None, None

def update_ticker_info(cursor, symbol, industry, sector, sub_category):
    cursor.execute("""
        UPDATE tickers
        SET ib_industry = ?, ib_sector = ?, ib_sub_sector = ?
        WHERE symbol = ?
    """, (industry, sector, sub_category, symbol))

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

    cursor.execute("SELECT symbol FROM tickers LIMIT 20")
    rows = cursor.fetchall()

    for row in rows:
        symbol = row[0]
        logging.info(f"Processing symbol: {symbol}")
        industry, sector, sub_category = get_industry_sector(ib, symbol)
        if industry and sector and sub_category:
            logging.info(f"Updating symbol: {symbol} with industry: {industry}, sector: {sector}, sub_category: {sub_category}")
            update_ticker_info(cursor, symbol, industry, sector, sub_category)
            conn.commit()

    ib.disconnect()
    conn.close()

if __name__ == "__main__":
    # Copilot keep start
    import sys    
    sys.argv = ['ib_sectors.py', '--host', '192.168.1.51', '--port', '7496', '--db', 'db/sqlite/tickers.sqlite']
    # Copilot keep end
    
    parser = argparse.ArgumentParser(description='Get industry sector information.')
    parser.add_argument('--host', type=str, required=True, help='Host IP address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--db', type=str, required=True, help='Database file path')
    args = parser.parse_args()

    main(args)
