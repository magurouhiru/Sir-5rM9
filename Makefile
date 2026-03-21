.PHONY: docs
VERSION := $(shell uv run tomlq '.project.version' pyproject.toml | tr -d '"')

docs:
	pdoc -f -o ./docs sir_5rm9

update:
	poetry update

image: image_version image_latest

image_version:
	docker build -t sir_5rm9:$(VERSION) .

image_latest:
	docker build -t sir_5rm9:latest .

push_image_latest:
	docker build --push -t sir_5rm9:latest .
