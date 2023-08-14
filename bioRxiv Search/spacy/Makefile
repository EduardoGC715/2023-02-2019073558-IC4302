.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)
# Para desarrollo
# make run
# dentro del bash, se pone python bioRxivAPI.py para correr el codigo
# cd "C:\Users\dandi\BasesII\Trabajos en Grupo\2023-02-2019073558-IC4302\bioRxiv Search"
run:
	docker run -itd --name spacydev --network rabbitnet -v "$(MY_DIR)":/app --env-file env-variables.txt crawlerimagedev:latest
	docker exec -it spacydev /bin/sh

start:
	docker start spacydev
	docker exec -it spacydev /bin/sh

stop:
	docker stop spacydev

# Mandar version
# make build version=1 (o 2 o x.)
build:
	@echo "Building..."
	docker build -t spacyimagedev:$(version) -f Dockerfile.dev .

	docker tag spacyimagedev:$(version) spacyimagedev:latest

runProd:
	docker start -d spacy

stopProd:
	docker stop spacy

buildProd:
	@echo "Building..."
	docker build -t spacyimage:$(version) .

	docker tag spacyimage:$(version) spacyimage:latest
	docker tag spacyimage:$(version) dandiego235/spacybio:$(version)
	docker tag spacyimage:$(version) dandiego235/spacybio:latest

push:
	docker push dandiego235/spacybio:$(version)
	docker push dandiego235/spacybio:latest