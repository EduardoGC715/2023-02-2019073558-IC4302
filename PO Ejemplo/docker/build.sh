#!/bin/bash
sudo docker login
cd componente1
sudo docker build -t nereo08/componente1 .
#sudo docker images
sudo docker push nereo08/componente1
cd ..
cd componente2
sudo docker build -t nereo08/componente2 .
#sudo docker images
sudo docker push nereo08/componente2
cd ..
cd componente3
sudo docker build -t nereo08/componente3 .
#sudo docker images
sudo docker push nereo08/componente3
cd ..
cd componente4
sudo docker build -t nereo08/componente4 .
#sudo docker images
sudo docker push nereo08/componente4
cd ..
cd componente5
sudo docker build -t nereo08/componente5 .
#sudo docker images
sudo docker push nereo08/componente5
cd ..

