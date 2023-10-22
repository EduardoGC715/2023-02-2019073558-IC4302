#!/bin/bash
# https://devopscube.com/install-configure-postgresql-amazon-linux/
DATE=$(date '+%Y%m%d%H%M')

mkdir -p /neo4j/$DATE
yum update -y

rpm --import https://debian.neo4j.com/neotechnology.gpg.key
cat << EOF >  /etc/yum.repos.d/neo4j.repo
[neo4j]
name=Neo4j RPM Repository
baseurl=https://yum.neo4j.com/stable/5
enabled=1
gpgcheck=1
EOF

yum install neo4j-5.12.0 -y

pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER -p $POSTGRES_PORT -w -c $POSTGRES_DB > /pgdump/$DATE/$POSTGRES_DB-$DATE.sql
echo "Backed up"
aws s3 cp /neo4j/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /neo4j/$DATE
echo "Finished!"
