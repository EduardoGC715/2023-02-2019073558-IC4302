IMAGE = flask-postgresqlha

build:
	@echo "Building..."
	docker build . --no-cache -t "${IMAGE}:$(version)"

	docker tag ${IMAGE}:$(version) ${IMAGE}:latest
	docker tag ${IMAGE}:$(version) dado715/${IMAGE}:$(version)
	docker tag ${IMAGE}:$(version) dado715/${IMAGE}:latest

publish:
	docker push "dado715/${IMAGE}:$(version)"
	docker push dado715/${IMAGE}:latest