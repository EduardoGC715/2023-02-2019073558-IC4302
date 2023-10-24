#!/bin/bash
# https://devopscube.com/install-configure-postgresql-amazon-linux/
DIRECTORY="/neodump"
mkdir -p $DIRECTORY || echo "Failed to create directory"

yum update -y

yum update -y

rpm --import https://debian.neo4j.com/neotechnology.gpg.key
cat << EOF >  /etc/yum.repos.d/neo4j.repo
[neo4j]
name=Neo4j RPM Repository
baseurl=https://yum.neo4j.com/stable/5
enabled=1
gpgcheck=1
EOF

NEO4J_ACCEPT_LICENSE_AGREEMENT=yes yum install neo4j-enterprise-5.13.0 -y


aws s3 cp s3://$BUCKET_NAME/$BACKUP_PATH/$RESTORE_FILE $DIRECTORY
echo "Downloaded"

neo4j-admin database restore --from-path=$DIRECTORY/$RESTORE_FILE --to-path-data=$NEO4J_SERVICE:$NEO4J_PORT --verbose

# neo4j-admin database restore --from-path=/neo4j/202310232022/neo4j-2023-10-23T20-25-10.backup --to-path-data=databases-admin.default.svc.cluster.local:6362 --overwrite-destination --verbose

echo "Restored"
rm -rf $DIRECTORY/$RESTORE_FILE
echo "Finished!"