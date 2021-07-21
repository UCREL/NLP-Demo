.ONESHELL:
SHELL := /bin/bash

cmd = not_override

APP_NAME = nlp_demo
USER_ID = $(shell id -u)
GROUP_ID = $(shell id -g)
export APP_NAME USER_ID GROUP_ID cmd

create_app:
	@mkdir -p ${APP_NAME}
	@DOCKER_BUILDKIT=1 docker build -t nlp_demo_dev_app:0.0.1 -f dev_app.dockerfile --build-arg USER_ID --build-arg GROUP_ID . 
	@docker-compose up create-app
	docker-compose down

run_app:
	@DOCKER_BUILDKIT=1 docker build -t nlp_demo_dev_app:0.0.1 -f dev_app.dockerfile --build-arg USER_ID --build-arg GROUP_ID . 
	@docker-compose up run-app
	docker-compose down

interact_app:
	@DOCKER_BUILDKIT=1 docker build -t nlp_demo_dev_app:0.0.1 -f dev_app.dockerfile --build-arg USER_ID --build-arg GROUP_ID . 
	@docker-compose up interact-app
	docker-compose down

profile-server-build-app:
	@DOCKER_BUILDKIT=1 docker build -t nlp_demo_build_app:0.0.1 -f build.dockerfile . 
	@docker-compose up profile-serve-built-app
	docker-compose down

build-app:
	@rm -rf nlp_demo/build
	@DOCKER_BUILDKIT=1 docker build -t nlp_demo_build_save_app:0.0.1 -f build-save.dockerfile --build-arg USER_ID --build-arg GROUP_ID . 
	@docker-compose up production-build-app
	docker-compose down
	