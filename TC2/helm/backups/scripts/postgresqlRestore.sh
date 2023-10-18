#!/bin/bash
# https://devopscube.com/install-configure-postgresql-amazon-linux/
DIRECTORY="/pgdump"
mkdir -p $DIRECTORY || echo "Failed to create directory"

yum update -y

amazon-linux-extras enable postgresql14
yum clean metadata
yum install postgresql -y

aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE $DIRECTORY
echo "Downloaded"

psql -h $POSTGRES_HOST -U $POSTGRES_USER -p $POSTGRES_PORT -w $POSTGRES_DB < $DIRECTORY/$RESTORE_FILE
echo "Restored"
rm -rf $DIRECTORY/$RESTORE_FILE
echo "Finished!"