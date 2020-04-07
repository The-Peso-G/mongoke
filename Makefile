


.PHONY: clean
clean:
	rm -rf generated

.PHONY: image
image:
	docker build . -t mongoke/mongoke
	docker push mongoke/mongoke

.PHONY: gcr
gcr:
	docker build . -t eu.gcr.io/molten-enigma-261612/mongoke
	docker push eu.gcr.io/molten-enigma-261612/mongoke

.PHONY: config-schema
config-schema:
	skema generate configuration_schema.skema --jsonschema ./mongoke/config_schema.json

.PHONY: generate-spec
generate-spec: clean
	python -m mongoke tests/confs/spec_conf.yaml --generated-path example_generated_code

.PHONY: play
play: generate-spec
	# MONGOKE_BASE_PATH=/path
	DB_URL=mongodb://localhost/db uvicorn --reload example_generated_code.__main__:app

.PHONY: test
test:
	docker-compose up -d mongo
	make generate-spec
	pytest -sv

