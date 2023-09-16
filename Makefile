DOCKER_TAG := latest
DOCKER_IMAGE := service
DOCKER_PORT := 4000
INTERNAL_PORT := 4040

run_app:
	python -m uvicorn src.app:main --host='0.0.0.0' --port=$(DOCKER_PORT)

docker_build:
	docker build \
		--tag ${DOCKER_IMAGE}:${DOCKER_TAG} .

docker_run:
	docker run \
		--detach \
		--publish ${INTERNAL_PORT}:${DOCKER_PORT} \
		--name ${DOCKER_IMAGE}_${INTERNAL_PORT} ${DOCKER_IMAGE}:${DOCKER_TAG}

lint:
	flake8 src/
