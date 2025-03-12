import argparse
from ib_async import Contract, IB

def get_industry_sector(symbol, exchange, currency, host, port):
    ib = IB()
    ib.connect(host=host, port=port)  # Connect to specified IP and port

    contract = Contract(symbol=symbol, secType="STK", exchange=exchange, currency=currency)

    contract_details = ib.reqContractDetails(contract)

    if contract_details:
        contract_detail = contract_details[0] # taking the first result.
        industry = contract_detail.industry
        sector = contract_detail.category
        sub_category = contract_detail.subcategory
        print(f"Symbol: {symbol}")
        # print industry-sector-category
        print(f"{industry}-{sector}-{sub_category}")
        #print(f"Industry: {industry}")
        #print(f"Sector: {sector}")
        
    else:
        print(f"Could not retrieve contract details for {symbol}.")

    ib.disconnect()

def main():
    parser = argparse.ArgumentParser(description='Get industry sector information.')
    parser.add_argument('--host', type=str, required=True, help='Host IP address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--db', type=str, required=True, help='Database file path')
    args = parser.parse_args()

    get_industry_sector("DDOG", "SMART", "USD", args.host, args.port)  # Example for Apple Inc.
    get_industry_sector("JPM", "SMART", "USD", args.host, args.port)  # Example for Alphabet Inc.
    get_industry_sector("APD", "SMART", "USD", args.host, args.port)

if __name__ == "__main__":
    main()
