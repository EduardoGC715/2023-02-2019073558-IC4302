.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)
# Para desarrollo
# make run
# dentro del bash, se pone python controller.py para correr el codigo
# cd "C:\Users\dandi\BasesII\Trabajos en Grupo\2023-02-2019073558-IC4302\bioRxiv Search"
run:
	docker run -itd -p 5673:5672 --name controllerdev --network rabbitnet -v "$(MY_DIR)":/app --env-file env-variables.txt controlimagedev:latest
	docker exec -it controllerdev /bin/sh

start:
	docker start controllerdev
	docker exec -it controllerdev /bin/sh

stop:
	docker stop controllerdev

# Mandar version
# make build version=1 (o 2 o x.)
build:
	@echo "Building..."
	docker build -t controlimagedev:$(version) -f Dockerfile.dev .

	docker tag controlimagedev:$(version) controlimagedev:latest

runProd:
	docker start -d controller

stopProd:
	docker stop controller

buildProd:
	@echo "Building..."
	docker build -t controlimage:$(version) .

	docker tag controller:$(version) controlimage:latest

	docker create --name controller -v .:/app controlimage:latest