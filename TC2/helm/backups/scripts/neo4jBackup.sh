#!/bin/bash
# https://devopscube.com/install-configure-postgresql-amazon-linux/
DATE=$(date '+%Y%m%d%H%M')

mkdir -p /neo4j/$DATE
touch /neo4j/$DATE/backup.cypher
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

curl -X POST http://databases-admin.default.svc.cluster.local:7474/db/neo4j/tx/commit -H "Content-Type:application/json" -d "{\"statements\":[{\"statement\":\"WITH 'backup.graphml' AS filename CALL apoc.export.graphml.all(filename, {useTypes:TRUE, storeNodeIds:FALSE}) YIELD file RETURN file;\"}]}" -H "Authorization: Basic bmVvNGo6bmVvNGotcGFzc3dvcmQ=" > /neo4j/$DATE/backup.graphml

curl --verbose POST http://databases-admin.default.svc.cluster.local:7474/db/neo4j/tx/commit -H "Content-Type:application/json" -d "{\"statements\":[{\"statement\":\"CALL apoc.export.cypher.all('backup.cypher', {useTypes: TRUE, storeNodeIds: FALSE})\"}]}" -H "Authorization: Basic bmVvNGo6bmVvNGotcGFzc3dvcmQ=" > /neo4j/$DATE/backup.cypher


echo "Backed up"
aws s3 cp /neo4j/$DATE s3://$BUCKET_NAME/$BACKUP_PATH/ --recursive
aws s3 ls s3://$BUCKET_NAME/$BACKUP_PATH/
rm -rf /neo4j/$DATE
echo "Finished!"
