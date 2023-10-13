.DEFAULT_GOAL: run
.PHONY: run build

MY_DIR := $(shell cd)

# Mandar version
# make build version=1 (o 2 o x.)


build:
	@echo "Building..."
	docker build -t wikiui:$(version) .

	docker tag wikiui:$(version) wikiui:latest
	docker tag wikiui:$(version) dandiego235/wikiui:$(version)
	docker tag wikiui:$(version) dandiego235/wikiui:latest

push:
	docker push dandiego235/wikiui:$(version)
	docker push dandiego235/wikiui:latest