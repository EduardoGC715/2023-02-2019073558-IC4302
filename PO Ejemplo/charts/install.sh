#!/bin/bash
#helm repo add elastic https://helm.elastic.co
#helm repo add bitnami https://charts.bitnami.com
#helm repo update

cd bootstrap
rm -rf Char.lock
helm dependency build --skip-refresh
cd ../stateful
rm -rf Char.lock
helm dependency build --skip-refresh
cd ..
helm upgrade --install bootstrap bootstrap
sleep 20
helm upgrade --install stateful stateful
sleep 60
helm upgrade --install stateless stateless
