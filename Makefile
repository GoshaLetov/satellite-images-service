DOCKER_TAG := latest
DOCKER_IMAGE := service
DOCKER_PORT := 5000
INTERNAL_PORT := 5050

run_app:
	PYTHONPATH=. python src/app.py


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
