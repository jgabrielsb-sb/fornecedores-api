#!/usr/bin/env sh
set -e

echo ""
echo "──────────────────────────────────────────────"
echo "  Fornecedores API - Entrypoint"
echo "──────────────────────────────────────────────"
echo ""

if [ -n "$DATABASE_HOST" ] && [ -n "$DATABASE_PORT" ]; then
  echo "Waiting for database at $DATABASE_HOST:$DATABASE_PORT..."
  until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
      sleep 1
  done
  echo "Database is available!"
fi

echo "Running Alembic migrations..."
alembic upgrade head
echo "Migrations completed."
echo ""

if [ "$DB_INSERT_INITIAL_DATA" = "true" ]; then
  echo "Inserting initial data..."
  make db-insert-initial-data || {
    echo "Failed to insert initial data."
    exit 1
  }
  echo "Initial data completed."
  echo ""
fi

echo "Starting API with Uvicorn..."
exec uvicorn src.run_api:app --host 0.0.0.0 --port 8000
