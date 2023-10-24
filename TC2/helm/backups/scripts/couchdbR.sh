#!/bin/bash
DIRECTORY="/couchdump/"
mkdir -p $DIRECTORY || echo "Failed to create directory"

yum update -y
yum install php-curl -y
yum install jq -y

aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE $DIRECTORY
echo "Downloaded"

FILE_PATH="$DIRECTORY/$RESTORE_FILE"

jq 'del(.docs[]._rev)' $FILE_PATH > "${FILE_PATH}_processed"
mv "${FILE_PATH}_processed" $FILE_PATH

URL="http://$COUCHDB_USER:$COUCHDB_PSW@$COUCHDB_HOST:$COUCHDB_PORT/$COUCHDB_DB/_bulk_docs"
curl -X POST "$URL" -H "Content-Type: application/json" --data "@$FILE_PATH"
echo "Restored"

rm -rf $FILE_PATH
echo "Finished!"