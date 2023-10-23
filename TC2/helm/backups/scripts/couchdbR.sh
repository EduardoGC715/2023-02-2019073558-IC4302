#!/bin/bash

# Directory to save the downloaded backup
DIRECTORY="/couchdump/"
mkdir -p $DIRECTORY || echo "Failed to create directory"

# Install necessary tools
yum update -y
yum install php-curl -y
yum install jq -y

# Download the specified backup file from S3 to the local directory
aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE $DIRECTORY
echo "Downloaded"

# The file will be stored in the DIRECTORY, so we set the full path to the downloaded file.
FILE_PATH="$DIRECTORY/$RESTORE_FILE"

# Remove _rev fields using jq
jq 'del(.docs[]._rev)' $FILE_PATH > "${FILE_PATH}_processed"
mv "${FILE_PATH}_processed" $FILE_PATH

# Restore the database
URL="http://$COUCHDB_USER:$COUCHDB_PSW@$COUCHDB_HOST:$COUCHDB_PORT/$COUCHDB_DB/_bulk_docs"
curl -X POST "$URL" -H "Content-Type: application/json" --data "@$FILE_PATH"
echo "Restored"

# Cleanup
rm -rf $FILE_PATH
echo "Finished!"
