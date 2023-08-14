.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)
# Para desarrollo
# make run
# dentro del bash, se pone python bioRxivAPI.py para correr el codigo
# cd "C:\Users\dandi\BasesII\Trabajos en Grupo\2023-02-2019073558-IC4302\bioRxiv Search"
run:
	docker run -itd --name crawlerdev --network rabbitnet -v "$(MY_DIR)":/app --env-file env-variables.txt crawlerimagedev:latest
	docker exec -it crawlerdev /bin/sh

start:
	docker start crawlerdev
	docker exec -it crawlerdev /bin/sh

stop:
	docker stop crawlerdev

# Mandar version
# make build version=1 (o 2 o x.)
build:
	@echo "Building..."
	docker build -t crawlerimagedev:$(version) -f Dockerfile.dev .

	docker tag crawlerimagedev:$(version) crawlerimagedev:latest

runProd:
	docker start -d crawler

stopProd:
	docker stop crawler

buildProd:
	@echo "Building..."
	docker build -t crawlerimage:$(version) .

	docker tag crawlerimage:$(version) crawlerimage:latest
	docker tag crawlerimage:$(version) dandiego235/crawlerbio:$(version)
	docker tag crawlerimage:$(version) dandiego235/crawlerbio:latest

push:
	docker push dandiego235/crawlerbio:$(version)
	docker push dandiego235/crawlerbio:latest