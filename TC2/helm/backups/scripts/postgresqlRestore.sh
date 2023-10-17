#!/bin/bash
# https://devopscube.com/install-configure-postgresql-amazon-linux/
DATE=$(date '+%Y%m%d%H%M')

mkdir -p /pgdump/$DATE
yum update

amazon-linux-extras enable postgresql14
yum clean metadata
yum install postgresql -y

# echo "$POSTGRES_HOST:$POSTGRES_PORT:$POSTGRES_DB:$POSTGRES_USER:$POSTGRES_PASSWORD" > ~/.pgpass
# chmod 0600 ~/.pgpass

# echo $PGPASSWORD

aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE /pgdump/$DATE --recursive
echo "Downloaded"

psql -h $POSTGRES_HOST -U $POSTGRES_USER -p $POSTGRES_PORT -w $POSTGRES_DB < /pgdump/$DATE/$RESTORE_FILE
echo "Restored"
rm -rf /pgdump/$DATE
echo "Finished!"