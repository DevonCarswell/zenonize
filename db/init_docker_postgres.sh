#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print each command before executing it

# Log file for debugging
LOG_FILE="/tmp/init_docker_postgres.log"

# Redirect stdout and stderr to the log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Starting PostgreSQL initialization script..."

# Check if the SQL file exists
if [ -f "/tmp/psql_data/zenonize.sql" ]; then
    echo "Found zenonize.sql, restoring database..."
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/psql_data/zenonize.sql
    echo "Database restored successfully."
else
    echo "Error: zenonize.sql not found in /tmp/psql_data/"
    exit 1
fi

echo "PostgreSQL initialization script completed."