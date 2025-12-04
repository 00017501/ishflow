#!/bin/bash

# Production Entrypoint Script for Ishflow Application
set -o errexit
set -o pipefail
set -o nounset

echo "Starting Django application in production environment"

# Change to the /app directory where the application is located.
cd /app

# Run database migrations.
make migrate

# Create test users.
echo "👥 Creating test users..."
make create_test_users

# Create default groups.
echo "👥 Creating default user groups..."
make create_default_groups

# Start the Django application.
echo "🚀 Running the Django application on Gunicorn..."
make run_server_prod

# Execute the command provided as arguments to this script, if any.
exec "$@"
