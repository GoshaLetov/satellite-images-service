APP_PORT := 5000
APP_HOST := '0.0.0.0'
SERVICE_PORT := 4000

.PHONY: start
start:
	python -m uvicorn src.app:main --host=$(APP_HOST) --port=$(APP_PORT)

.PHONY: build
build:
	docker build --tag $(DOCKER_IMAGE):$(DOCKER_TAG) .

.PHONY: push
push:
	docker login -u $(CI_DOCKER_REGISTRY_USER) -p $(CI_DOCKER_REGISTRY_PASSWORD) $(CI_DOCKER_REGISTRY)
	docker push $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: deploy
deploy:
	ansible-playbook -i deploy/inventory.ini deploy/deploy.yml \
		-e docker_image=$(DOCKER_IMAGE) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry=$(CI_DOCKER_REGISTRY) \
		-e docker_registry_user=$(CI_DOCKER_REGISTRY_USER) \
		-e docker_registry_password=$(CI_DOCKER_REGISTRY_PASSWORD)

.PHONY: destroy
destroy:
	ansible-playbook -i deploy/inventory.ini deploy/destroy.yml

.PHONY: run
run:
	docker run \
		--detach \
		--publish $(SERVICE_PORT):$(APP_PORT) \
		--name $(DOCKER_TAG).$(INTERNAL_PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: lint
lint:
	flake8 src/
