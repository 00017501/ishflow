#!/bin/sh
set -e

echo "Starting Certbot entrypoint script..."

# Wait for nginx to be ready
echo "Waiting for nginx to start..."
sleep 15

# Check if certificates already exist
if [ -f "/etc/letsencrypt/live/ishflow.uz/fullchain.pem" ]; then
    echo "Certificates already exist. Starting renewal loop..."
else
    echo "Certificates not found. Obtaining new certificates..."

    # Request certificates
    certbot certonly \
        --webroot \
        --webroot-path=/var/www/certbot \
        --email info@ishflow.uz \
        --agree-tos \
        --no-eff-email \
        -d ishflow.uz \
        -d www.ishflow.uz

    if [ $? -eq 0 ]; then
        echo "Certificates obtained successfully!"
        echo "HTTPS will be enabled on next nginx reload."
        echo "Please run: docker-compose restart nginx"
    else
        echo "Failed to obtain certificates. Will retry on next run."
    fi
fi

# Auto-renewal loop (check twice daily)
while :; do
    echo "Sleeping for 12 hours before next renewal check..."
    sleep 12h

    echo "Attempting certificate renewal..."
    certbot renew --deploy-hook "echo 'Certificate renewed. Please reload nginx manually.'"
done
