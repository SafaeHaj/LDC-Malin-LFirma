DOCKER_COMPOSE_FILE = docker-compose.yaml

all:
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up

down:
	@docker-compose -f ${DOCKER_COMPOSE_FILE} down
