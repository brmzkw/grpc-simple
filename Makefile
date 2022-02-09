up: build proto
	docker-compose up

shell-client:
	docker-compose run --no-deps --rm --name client client bash

shell-server:
	docker-compose run --no-deps --rm --name server server bash

build:
	docker-compose build

.PHONY: proto
proto:
	docker-compose run --no-deps --rm server \
		poetry run \
		python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. ./myapp/calculator.proto
