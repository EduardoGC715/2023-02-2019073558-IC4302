.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)

# Mandar version
# make build version=1 (o 2 o x.)



build:
	@echo "Building..."
	docker build -t wikiapi:$(version) .

	docker tag wikiapi:$(version) wikiapi:latest
	docker tag wikiapi:$(version) dandiego235/wikiapi:$(version)
	docker tag wikiapi:$(version) dandiego235/wikiapi:latest

push:
	docker push dandiego235/wikiapi:$(version)
	docker push dandiego235/wikiapi:latest