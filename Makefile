#!make
include .env
.DEFAULT_GOAL=up
MAKEFLAGS += --no-print-directory

# Constants
TAIL_LOGS = 50
TEST_WORKERS = auto
PYLINT_FAIL_UNDER = 8

prepare-env:
	$s cp -n .env-dist .env

up: prepare-env
	$s docker compose up --force-recreate -d

down:
	$s docker compose down

down-up: down up

up-build: down build up

build: prepare-env
	$s docker compose build

complete-build: build down-up
logs:
	$s cd ./docker && docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_backend

bash:
	$s cd ./docker && docker exec -it ${PROJECT_NAME}_backend bash

sh:
	$s cd ./docker && docker exec -it ${PROJECT_NAME}_backend bash

shell:
	$s cd ./docker && docker exec -it ${PROJECT_NAME}_backend python manage.py shell_plus

