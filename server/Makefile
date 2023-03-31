build: # Build containers with the server. Usage: "make build"
	@touch .app.env
	@touch .mongoExpress.env
	@docker-compose build

up: # Up containers with the server. Usage: "make up [SALT=YOUR_SALT] [ME_USER=USER_FOR_MONGO_EXPRESS] [ME_PASSWORD=PASSWORD_FOR_MONGO_EXPRESS]". ME_USER default is "user", ME_PASSWORD default is "userIsAbobus".
	@rm -f .app.env
	@touch .app.env
	@if [ $(SALT) ]; then\
		echo SALT=$(SALT) >> .app.env;\
	fi
	@rm -f .mongoExpress.env
	@touch .mongoExpress.env
	@if [ $(ME_USER) ]; then\
		echo ME_CONFIG_BASICAUTH_USERNAME=$(ME_USER) >> .mongoExpress.env;\
	else\
		echo ME_CONFIG_BASICAUTH_USERNAME=user >> .mongoExpress.env;\
	fi
	@if [ $(ME_PASSWORD) ]; then\
		echo ME_CONFIG_BASICAUTH_PASSWORD=$(ME_PASSWORD) >> .mongoExpress.env;\
	else\
		echo ME_CONFIG_BASICAUTH_PASSWORD=userIsAbobus >> .mongoExpress.env;\
	fi

	@docker-compose up -d

stop: # Stop containers with the server. Usage: "make stop"
	@touch .app.env
	@docker-compose stop

down: # Down containers with the server. Usage: "make down"
	@touch .app.env
	@touch .mongoExpress.env
	@docker-compose down

get_salt: # Get the salt setted to signer. Usage: "make get_salt"
	@docker logs server-app 2>&1 | grep "Salt of signer setted to:"

help: # Show help for each of the Makefile recipes. Usage: "make help"
	@grep -E '^[a-zA-Z0-9 -_]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
