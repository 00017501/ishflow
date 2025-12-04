#!/usr/bin/env bash

set -e

domains="ishflow.uz www.ishflow.uz assets.ishflow.uz"
email="admin@ishflow.uz"
staging=0 # Set to 1 if you want to test with staging server first

echo "### Requesting Let's Encrypt certificates for: ${domains}"

if [ $staging != "0" ]; then
  staging_arg="--staging"
  echo "Using Let's Encrypt staging server"
else
  staging_arg=""
  echo "Using Let's Encrypt production server"
fi

# Get certificates for ishflow.uz
echo "### Requesting certificate for ishflow.uz..."
docker compose -f docker/compose/prod.yaml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email $email \
  --agree-tos \
  --no-eff-email \
  $staging_arg \
  -d ishflow.uz \
  -d www.ishflow.uz

# Get certificates for assets.ishflow.uz
echo "### Requesting certificate for assets.ishflow.uz..."
docker compose -f docker/compose/prod.yaml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email $email \
  --agree-tos \
  --no-eff-email \
  $staging_arg \
  -d assets.ishflow.uz

echo "### Reloading Nginx..."
docker compose -f docker/compose/prod.yaml exec nginx nginx -s reload

echo "### SSL certificates obtained successfully!"
echo "Certbot will automatically renew certificates every 12 hours."
