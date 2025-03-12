#!/bin/bash

DATABASE_FILE="db/sqlite/tickers.sqlite"
HOST=192.168.1.51
PORT=7496

# 1. POC using uvx, python with ib_async..
# 2. Try generate python/js version with IB WebAPI using AI only (based on first script)

uvx ./ib_sectors.py --host $HOST --port $PORT --db $DATABASE_FILE
