.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)
# Para desarrollo
# make run
# dentro del bash, se pone python controller.py para correr el codigo
# cd "C:\Users\dandi\BasesII\Trabajos en Grupo\2023-02-2019073558-IC4302\bioRxiv Search"
run:
	docker run -itd --name loaderdev -v "$(MY_DIR)":/app wikiloaderdev:latest
	docker exec -it loaderdev /bin/sh

start:
	docker start loaderdev
	docker exec -it loaderdev /bin/sh

stop:
	docker stop loaderdev

# Mandar version
# make build version=1 (o 2 o x.)
build:
	@echo "Building..."
	docker build -t wikiloaderdev:$(version) -f Dockerfile.dev .

	docker tag wikiloaderdev:$(version) wikiloaderdev:latest

runProd:
	docker start -d wikiloader

stopProd:
	docker stop wikiloader

buildProd:
	@echo "Building..."
	docker build -t wikiloader:$(version) .

	docker tag wikiloader:$(version) wikiloader:latest
	docker tag wikiloader:$(version) dandiego235/wikiloader:$(version)
	docker tag wikiloader:$(version) dandiego235/wikiloader:latest

push:
	docker push dandiego235/wikiloader:$(version)
	docker push dandiego235/wikiloader:latest