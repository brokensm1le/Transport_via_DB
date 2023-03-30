build: # Build containers with the local server. Usage: "make build"
	@docker-compose build

up: # Up containers with the local server. Usage: "make up SALT=YOUR_SALT PATH_PUB_KEY=YOUR_PATH_PUB_KEY PATH_PRV_KEY=YOUR_PATH_PRV_KEY ADDR_SERVER=YOUR_ADDR_SERVER"
	@rm -f .env
	@touch .env
	@if [ $(SALT) ]; then\
		echo SALT=$(SALT)\n >> .env;\
	else\
		echo No SALT variable.;\
		$(eval BAD_ARGS=1)\
	fi
	@if [ $(PATH_PUB_KEY) ]; then\
		if test -f "$(PATH_PUB_KEY)"; then\
			echo PATH_PUB_KEY=$(PATH_PUB_KEY) >> .env;\
		else\
			echo \"$(PATH_PUB_KEY)\" is not a valid path to public key file.;\
			$(eval BAD_ARGS=1)\
		fi;\
	else\
		echo No PATH_PUB_KEY variable.;\
		$(eval BAD_ARGS=1)\
	fi
	@if [ $(PATH_PRV_KEY) ]; then\
		if test -f "$(PATH_PRV_KEY)"; then\
			echo PATH_PRV_KEY=$(PATH_PRV_KEY) >> .env;\
		else\
			echo \"$(PATH_PRV_KEY)\" is not a valid path to private key file.;\
			$(eval BAD_ARGS=1)\
		fi;\
	else\
		echo No PATH_PRV_KEY variable.;\
		$(eval BAD_ARGS=1)\
	fi
	@if [ $(ADDR_SERVER) ]; then\
		echo ADDR_SERVER=$(ADDR_SERVER) >> .env;\
	else\
		echo No ADDR_SERVER variable.;\
		$(eval BAD_ARGS=1)\
	fi
	
	@if [ $(BAD_ARGS) ]; then\
		exit 1;\
	fi
	@docker-compose up -d

stop: # Stop containers with the local server. Usage: "make stop"
	@docker-compose stop

down: # Down containers with the local server. Usage: "make down"
	@docker-compose down

help: # Show help for each of the Makefile recipes. Usage: "make help"
	@grep -E '^[a-zA-Z0-9 -_]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
