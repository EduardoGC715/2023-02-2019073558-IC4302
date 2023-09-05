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
	docker build -t postgreflask:$(version) .

	docker tag postgreflask:$(version) postgreflask:latest
	docker tag postgreflask:$(version) dandiego235/postgreflask:$(version)
	docker tag postgreflask:$(version) dandiego235/postgreflask:latest

push:
	docker push dandiego235/postgreflask:$(version)
	docker push dandiego235/postgreflask:latest