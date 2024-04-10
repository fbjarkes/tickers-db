#!/bin/bash

#set -x

MIGRATIONS_PATH="migrations"
DATABASE_FILE="$(realpath tickers.sqlite)"

# Create migrations table if it doesn't exist
sqlite3 "$DATABASE_FILE" "CREATE TABLE IF NOT EXISTS migrations (name TEXT PRIMARY KEY);"

# Change to the migrations directory
pushd "$MIGRATIONS_PATH" || exit

# Get all migration files in order
MIGRATION_FILES=$(ls migration_*.sql | sort)

for FILE in $MIGRATION_FILES; do
  # Extract the migration name from the file name
  MIGRATION_NAME=$(basename "$FILE" .sql)
  echo "Verifying migration '$MIGRATION_NAME'..."  
  if ! sqlite3 "$DATABASE_FILE" "SELECT name FROM migrations WHERE name = '$MIGRATION_NAME';" | grep -q "$MIGRATION_NAME"; then
    echo "Applying migration '$MIGRATION_NAME'..."
    if ! sqlite3 "$DATABASE_FILE" < "$FILE"; then
        echo "Migration '$MIGRATION_NAME' failed."
        exit 1
    fi
    # Record that the migration has been applied
    sqlite3 "$DATABASE_FILE" "INSERT INTO migrations (name) VALUES ('$MIGRATION_NAME');"
    echo "Migration '$MIGRATION_NAME' applied."
  fi
done

# Return to the original directory
popd || exit