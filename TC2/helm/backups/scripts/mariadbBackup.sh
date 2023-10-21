#!/bin/bash

DATE=$(date '+%Y%m%d%H%M')

mkdir -p /mariadbdump/$DATE
yum update -y

# Install MariaDB client
yum install mariadb -y

# Perform the backup
mysqldump -h $MARIA_CONNECTION_STRING -u root -p$MARIA_PASSWORD pokemon_db > /mariadbdump/$DATE/pokemon_db-$DATE.sql

# Upload to S3
aws s3 cp /mariadbdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive

# Clean up
rm -rf /mariadbdump/$DATE

echo "Backup Finished!"