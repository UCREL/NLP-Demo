.ONESHELL:
SHELL := /bin/bash

cmd = not_override

APP_NAME = nlp_demo
USER_ID = $(shell id -u)
GROUP_ID = $(shell id -g)
export APP_NAME USER_ID GROUP_ID cmd


create_app:
	@docker-compose up create-app
	docker-compose down

run_app:
	@docker-compose up run-app
	docker-compose down

build_app:
	@docker-compose up build-app
	docker-compose down

interact_app:
	@docker-compose up interact-app
	docker-compose down

profile-and-server-app:
	@docker-compose up profile-and-serve-built-app
	docker-compose down
	