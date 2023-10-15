#!/bin/bash
DATE=$(date '+%Y%m%d%H%M')
mkdir -p /mongodump/$DATE
yum update

cat <<EOT > /etc/yum.repos.d/mongodb-org-7.0.repo
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOT
yum update
yum install mongodb-database-tools -y
mongodump --host="$MONGO_CONNECTION_STRING" -u $MONGO_USERNAME -p $MONGO_PASSWORD --gzip --archive=/mongodump/$DATE
aws s3 cp /mongodump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /mongodump/$DATE