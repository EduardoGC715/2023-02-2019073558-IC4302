#!/bin/bash
#helm repo add elastic https://helm.elastic.co
#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo add couchdb https://apache.github.io/couchdb-helm
#helm repo add neo4j https://helm.neo4j.com/neo4j
#helm repo update

cd bootstrap
rm -rf Chart.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install bootstrap bootstrap
sleep 20
cd databases
rm -rf Chatr.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install databases databases
sleep 60
cd backups
rm -rf Chart.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install backups backups

