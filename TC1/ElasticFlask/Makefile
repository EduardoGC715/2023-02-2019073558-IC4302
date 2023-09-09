.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)

# Mandar version
# make build version=1 (o 2 o x.)

run:
	docker start -d controller

stop:
	docker stop controller

build:
	@echo "Building..."
	docker build -t elasticflask:$(version) .

	docker tag elasticflask:$(version) elasticflask:latest
	docker tag elasticflask:$(version) dandiego235/elasticflask:$(version)
	docker tag elasticflask:$(version) dandiego235/elasticflask:latest

push:
	docker push dandiego235/elasticflask:$(version)
	docker push dandiego235/elasticflask:latest