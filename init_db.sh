#!/bin/bash - 
#===============================================================================
#
#          FILE: init_db.sh
# 
#         USAGE: ./init_db.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 03/12/2024 11:35
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

NASDAQ="data/nasdaqlisted.txt"
OTHER="data/otherlisted.txt"
DATABASE_FILE="db/sqlite/tickers.sqlite"
TICKERS_SCHEMA_FILE="db/sqlite/tickers_schema.sql"

# ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt and ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt
#curl ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt > $OTHER
#curl ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt > $NASDAQ


# Check if sqlite3 is available
if ! command -v sqlite3 &> /dev/null; then
  echo "Error: sqlite3 is not installed."
  exit 1
fi

# Check if database file exists
if [ ! -f "$DATABASE_FILE" ]; then
  # Create database with schema.sql
  sqlite3 "$DATABASE_FILE" < $TICKERS_SCHEMA_FILE
  echo "Database '$DATABASE_FILE' created."
fi


# 1. Process nasdaq data (ignore errors due to extra columns warning while importing)
sqlite3 "$DATABASE_FILE" <<EOF 2>/dev/null
.mode csv
.header on
.separator '|'

-- Import only the desired columns into the staging table
.import "$NASDAQ" staging_nasdaq

-- Insert data from staging table into the main table, applying REGEXP filter
INSERT OR IGNORE INTO tickers (symbol, company_name)
SELECT symbol, company_name FROM staging_nasdaq
WHERE LOWER(company_name) REGEXP 'ads|inc|common units|representing limited|Com+mon shares|share|american depositary shares|com+mon stock|ordinary shares';
EOF
echo "Data imported from '$NASDAQ' into the staging table."

# 2. Process other data (ignore errors due to extra columns warning while importing)
sqlite3 "$DATABASE_FILE" <<EOF 2>/dev/null
.mode csv
.header on
.separator '|'

-- Import only the desired columns into the staging table
.import "$OTHER" staging_other

-- Insert data from staging table into the main table, applying REGEXP filter
INSERT OR IGNORE INTO tickers (symbol, company_name)
SELECT symbol, company_name FROM staging_other
WHERE LOWER(company_name) REGEXP 'ads|inc|common units|representing limited|Com+mon shares|share|american depositary shares|com+mon stock|ordinary shares';
EOF
echo "Data imported from '$OTHER' into the staging table."



