build: # Build containers with the server. Usage: "make build"
	@touch .env
	@docker-compose build

up: # Up containers with the server. Usage: "make up [SALT=YOUR_SALT]"
	@rm -f .env
	@touch .env
	@if [ $(SALT) ]; then\
		echo SALT=$(SALT) >> .env;\
	fi
	@docker-compose up -d

stop: # Stop containers with the server. Usage: "make stop"
	@touch .env
	@docker-compose stop

down: # Down containers with the server. Usage: "make down"
	@touch .env
	@docker-compose down

get_salt: # Get the salt setted to signer. Usage: "make get_salt"
	@docker logs server-app 2>&1 | grep "Salt of signer setted to:"

help: # Show help for each of the Makefile recipes. Usage: "make help"
	@grep -E '^[a-zA-Z0-9 -_]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
