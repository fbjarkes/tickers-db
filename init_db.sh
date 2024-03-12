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
curl ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt > $OTHER
curl ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt > $NASDAQ


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


# 1. Process nasdaq data
sqlite3 "$DATABASE_FILE" <<EOF
.mode csv
.header on
-- Import only the desired columns
.import "$NASDAQ" companies
EOF
echo "Data imported from '$NASDAQ'."

# 2. Process other data



