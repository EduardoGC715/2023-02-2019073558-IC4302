#!/bin/bash

# Variables
RESTORE_DIR="/mariadbdump"

# Create directory for restore
mkdir -p $RESTORE_DIR || echo "Failed to create directory"

yum update -y

# Download backup files from S3
aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE $RESTORE_DIR
ls $RESTORE_DIR

# Install MariaDB client
yum install mariadb -y

# Restore the backup
mysql -h $MARIA_CONNECTION_STRING -u root -p$MARIA_PASSWORD pokemon_db < $RESTORE_DIR/$RESTORE_FILE

# Clean up restore directory
rm -rf $RESTORE_DIR

echo "Restore Finished!"