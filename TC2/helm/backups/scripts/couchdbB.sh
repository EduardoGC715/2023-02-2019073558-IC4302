#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /couchdump/$DATE
yum update 

yum install php-curl -y
yum install jq -y

URL="http://$COUCHDB_USER:$COUCHDB_PSW@$COUCHDB_HOST:$COUCHDB_PORT/$COUCHDB_DB/_all_docs?include_docs=true"
curl -X GET "$URL" -H "Accept: application/json" | jq '{ docs: [.rows[] | .doc] }' > /couchdump/$DATE/pokemonBackup.json
echo "Backed up"

aws s3 cp /couchdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /couchdump/$DATE
echo "Finished!"