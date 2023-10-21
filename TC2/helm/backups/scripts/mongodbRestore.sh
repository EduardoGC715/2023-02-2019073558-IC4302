#!/bin/bash
DIRECTORY="/mongodump"
mkdir -p $DIRECTORY || echo "Failed to create directory"

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
aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE/archive $DIRECTORY
echo "Downloaded"
mongorestore --host="$MONGO_CONNECTION_STRING" -u $MONGO_USERNAME -p $MONGO_PASSWORD --archive="$DIRECTORY/archive"