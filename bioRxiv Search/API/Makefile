.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)
# Para desarrollo
# make run
# dentro del bash, se pone python bioRxivAPI.py para correr el codigo
run:
	docker run -itd --name bioappdev -v "$(MY_DIR)":/app bioapidev:latest
	docker exec -it bioappdev /bin/sh

start:
	docker start bioappdev
	docker exec -it bioappdev /bin/sh

stop:
	docker stop bioappdev

# Mandar version
# make build version=1 (o 2 o x.)
build:
	@echo "Building..."
	docker build -t bioapidev:$(version) -f Dockerfile.dev .

	docker tag bioapidev:$(version) bioapidev:latest

runProd:
	docker start -d bioRxivAPI

stopProd:
	docker stop bioRxivAPI

buildProd:
	@echo "Building..."
	docker build -t bioRxivAPI:$(version) .

	docker tag bioRxivAPI:$(version) bioRxivAPI:latest

	docker create --name bioRxivAPI -v .:/app bioRxivAPI:latest