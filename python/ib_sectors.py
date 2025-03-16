# /// script
# requires-python = ">=3.12"
# dependencies = ["ib_async", "nest_asyncio"]
# ///


import argparse
import sqlite3
import logging
import asyncio
import nest_asyncio
from ib_async import Contract, IB, StartupFetch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IB_CONCURRENCY = 5
PROCESS_CHUNK_SIZE = 50

async def get_industry_sector(ib, symbol, exchange="SMART", currency="USD"):
    contract = Contract(symbol=symbol, secType="STK", exchange=exchange, currency=currency)
    contract_details = ib.reqContractDetails(contract)

    if contract_details:
        contract_detail = contract_details[0]  # taking the first result
        return contract_detail.industry, contract_detail.category, contract_detail.subcategory
    logging.warning(f"Could not retrieve contract details for {symbol}.")
    return None, None, None

async def process_updates(conn, cursor, updates, chunk_id):
    logging.info(f"Chunk-{chunk_id}: Processing updates for {len(updates)} records in")
    cursor.executemany("""
        UPDATE tickers
        SET ib_industry = ?, ib_sector = ?, ib_sub_sector = ?
        WHERE symbol = ?
    """, updates)
    conn.commit()
    logging.info(f"Chunk-{chunk_id}: Done processing updates.")

async def process_symbol(symbol, ib, semaphore):
    async with semaphore:
        #logging.info(f"{symbol}: fetching data...")
        industry, sector, sub_category = await get_industry_sector(ib, symbol)
        if industry and sector and sub_category:
            logging.info(f"{symbol}: industry: {industry}, sector: {sector}, sub_category: {sub_category}")        
            return industry, sector, sub_category, symbol
        return None, None, None, symbol

async def process_chunk(chunk, conn, ib, semaphore, cursor, chunk_id):
    tasks = [process_symbol(row[0], ib, semaphore) for row in chunk]
    res = await asyncio.gather(*tasks)
    
    # Filter out None results
    updates = [(industry, sector, sub_category, symbol) for industry, sector, sub_category, symbol in res if industry]
    await process_updates(conn, cursor, updates, chunk_id)

async def main(args):
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

    cursor.execute("SELECT symbol FROM tickers WHERE ib_industry IS NULL LIMIT 500")
    rows = cursor.fetchall()

    semaphore = asyncio.Semaphore(IB_CONCURRENCY)
    chunk_semaphore = asyncio.Semaphore(2)  # Limit concurrent chunk processing to 2

    async def process_chunk_with_semaphore(chunk, chunk_id):
        async with chunk_semaphore:
            await process_chunk(chunk, conn, ib, semaphore, cursor, chunk_id)

    chunks = [rows[i:i + PROCESS_CHUNK_SIZE] for i in range(0, len(rows), PROCESS_CHUNK_SIZE)]
    chunk_tasks = [process_chunk_with_semaphore(chunk, i) for i, chunk in enumerate(chunks)]    
    await asyncio.gather(*chunk_tasks)
    

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

    nest_asyncio.apply()
    asyncio.run(main(args))
