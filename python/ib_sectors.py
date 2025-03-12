import argparse
import sqlite3
from ib_async import Contract, IB

def get_industry_sector(ib, symbol, exchange, currency):
    contract = Contract(symbol=symbol, secType="STK", exchange=exchange, currency=currency)

    contract_details = ib.reqContractDetails(contract)

    if contract_details:
        contract_detail = contract_details[0] # taking the first result.
        industry = contract_detail.industry
        sector = contract_detail.category
        sub_category = contract_detail.subcategory
        return industry, sector, sub_category
    else:
        print(f"Could not retrieve contract details for {symbol}.")
        return None, None, None

def main():
    parser = argparse.ArgumentParser(description='Get industry sector information.')
    parser.add_argument('--host', type=str, required=True, help='Host IP address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--db', type=str, required=True, help='Database file path')
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.db)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    cursor = conn.cursor()

    ib = IB()
    if not ib.connect(host=args.host, port=args.port):  # Connect to specified IP and port
        print("Error connecting to IB")
        conn.close()
        return

    cursor.execute("SELECT symbol FROM tickers LIMIT 20")
    rows = cursor.fetchall()

    for row in rows:
        symbol = row[0]
        print(f"Processing symbol: {symbol}")  # Debug printing
        industry, sector, sub_category = get_industry_sector(ib, symbol, "SMART", "USD")
        if industry and sector and sub_category:
            print(f"Updating symbol: {symbol} with industry: {industry}, sector: {sector}, sub_category: {sub_category}")  # Debug printing
            cursor.execute("""
                UPDATE tickers
                SET ib_industry = ?, ib_sector = ?, ib_sub_sector = ?
                WHERE symbol = ?
            """, (industry, sector, sub_category, symbol))
            conn.commit()

    ib.disconnect()
    conn.close()

if __name__ == "__main__":
    import sys    
    sys.argv = ['ib_sectors.py', '--host', '192.168.1.51', '--port', '7496', '--db', 'db/sqlite/tickers.sqlite']
    main()
