


.PHONY: clean
clean:
	rm -rf generated

config-schema:
	skema generate configuration_schema.skema --jsonschema ./mongoke/config_schema.json

.PHONY: play
generate-spec: clean
	python -m mongoke tests/confs/spec_conf.yaml --generated-path example_generated_code

.PHONY: play
play: generate-spec
	python -m example_generated_code

.PHONY: play
tests: generate-pr
	pytest


