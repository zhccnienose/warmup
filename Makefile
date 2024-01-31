DIR = ${shell pwd}

CMD = $(DIR)/cmd

CONFIG_PATH = $(DIR)/config

IDL_PATH = $(DIR)/idl

OUTPUT_PATH = $(DIR)/output

SERVICES := template
service = $(word 1,$@)

MOCKS := user_mock
mock = $(word 1,$@)

PERFIX = "[Makefile]"

.PHONY: env-up
env-up:
	@ docker compose -f ./docker/docker-compose.yml up -d

.PHONY: $(SERVICES)
$(SERVICES):
	mkdir -p output
	cd $(CMD)/$(service) && sh build.sh
	cd $(CMD)/$(service)/output && cp -r . $(OUTPUT_PATH)/$(service)
	@echo "$(PERFIX) Build $(service) target completed"
ifndef autorun
	@echo "$(PERFIX) Automatic run server"
	sh entrypoint.sh $(service)
endif

.PHONY: clean
clean:
	@find . -type d -name "output" -exec rm -rf {} + -print

.PHONY: build-all
build_all:
	@for var in $(SERVICES);
			ECHO "$(PERFIX) building $var service"; \
			make $var autorun=1; \
	  done

.PHONY: docker
docker:
	docker build -t fzuhelper .
	sh docker-run.sh
