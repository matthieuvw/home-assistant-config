SHELL=/bin/bash

PUID := $(shell id -u)
GUID := $(shell id -g)

start:

	docker run -d \
		--name "hass-test" \
		-v  $(PWD):/config \
		-e TZ="Europe/Paris" \
		--net=host \
		-e PUID=${PUID} \
		-e GUID=${GUID} \
		homeassistant/home-assistant:latest

stop:

	docker stop hass-test && docker rm hass-test
	rm -f ./*.log
	rm -f ./*.db

logs:

	docker logs -f hass-test

clean-wa:

	rm -f ./*.log
	rm -f ./*.db

deep-clean:

	sudo rm -Rf .storage
	sudo rm -Rf .cloud
	sudo rm -f .HA_VERSION
	sudo rm -f ./*.log
	sudo rm -f ./*.db

restart: stop start
