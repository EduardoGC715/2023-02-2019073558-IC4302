#!/bin/bash
# https://devopscube.com/install-configure-postgresql-amazon-linux/
DATE=$(date '+%Y%m%d%H%M')

mkdir -p /pgdump/$DATE
yum update -y

amazon-linux-extras enable postgresql14
yum clean metadata
yum install postgresql -y

pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER -p $POSTGRES_PORT -w -c $POSTGRES_DB > /pgdump/$DATE/$POSTGRES_DB-$DATE.sql
echo "Backed up"
aws s3 cp /pgdump/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /pgdump/$DATE
echo "Finished!"
