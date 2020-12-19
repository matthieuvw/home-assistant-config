SHELL=/bin/bash

PUID := $(shell id -u)
GUID := $(shell id -g)

YOUR_HASS_CONFIG_DIRECTORY := $(shell pwd)
SOME_LOCAL_WORKSPACE=/tmp/pouet

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

ext-clean:

	rm -Rf $(SOME_LOCAL_WORKSPACE)
	rm -Rf $(YOUR_HASS_CONFIG_DIRECTORY)/custom_components/pyscript

ext-pyscript: ext-clean

	mkdir -p $(SOME_LOCAL_WORKSPACE)
	cd $(SOME_LOCAL_WORKSPACE)
	git -C $(SOME_LOCAL_WORKSPACE) clone https://github.com/custom-components/pyscript.git
	mkdir -p $(YOUR_HASS_CONFIG_DIRECTORY)/custom_components
	cp -pr $(SOME_LOCAL_WORKSPACE)/pyscript/custom_components/pyscript $(YOUR_HASS_CONFIG_DIRECTORY)/custom_components
