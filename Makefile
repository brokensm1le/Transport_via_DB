run_local_server: # Run local server. Usage: "make run_local_server SALT=YOUR_SALT PATH_PUB_KEY=YOUR_PATH_PUB_KEY PATH_PRV_KEY=YOUR_PATH_PRV_KEY ADDR_SERVER=YOUR_ADDR_SERVER"
	@(cd local_server && make -s build && make -s up SALT=$(SALT) PATH_PUB_KEY=$(PATH_PUB_KEY) PATH_PRV_KEY=$(PATH_PRV_KEY) ADDR_SERVER=$(ADDR_SERVER))

down_local_server: # Down local server. Usage: "make down_local_server"
	@(cd local_server && make -s down)

run_server: # Run server. Usage: "make run_server [SALT=YOUR_SALT]"
	@(cd server && make -s build && make -s up SALT=$(SALT) && sleep 1 && make -s get_salt)

down_server: # Down server. Usage: "make down_server"
	@(cd server && make -s down)

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -_]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
