#!/bin/bash

apt-get update
apt-get -y upgrade
apt-get -y install pip
apt-get remove  -y docker.io
apt-get remove  -y docker-doc
apt-get remove  -y docker-compose
apt-get remove  -y podman-docker
apt-get remove  -y containerd
apt-get remove  -y runc
apt-get remove  -y docker
apt-get install ca-certificates curl gnupg -y
apt-get install unzip -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg |  gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
mkdir "/home/ubuntu/app"

docker run -d -v "/home/ubuntu/app":/app/volume --name wikiloader dandiego235/wikiloader:10
docker run -d -p 3000:3000 --name wikiui dandiego235/wikiui:8
docker run -d -p 5000:5000 -p 8000:8000 --name wikiapi dandiego235/wikiapi:8
