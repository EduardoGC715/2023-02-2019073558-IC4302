#!/bin/bash
#helm repo add elastic https://helm.elastic.co
#helm repo add bitnami https://charts.bitnami.com/bitnami
#helm repo update

cd bootstrap
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install bootstrap bootstrap
sleep 20
cd databases
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install databases databases
sleep 60
cd backups
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install backups backups

