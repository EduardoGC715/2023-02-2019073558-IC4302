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
	docker build -t mongoflask:$(version) .

	docker tag mongoflask:$(version) mongoflask:latest
	docker tag mongoflask:$(version) dandiego2356/mongoflask:$(version)
	docker tag mongoflask:$(version) dandiego2356/mongoflask:latest

push:
	docker push dandiego2356/mongoflask:$(version)
	docker push dandiego2356/mongoflask:latest