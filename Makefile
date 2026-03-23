.PHONY: docs

docs:
	pdoc -f -o ./docs sir_5rm9

update:
	poetry update

image: image_latest

image_latest:
	docker build -t sir_5rm9:latest .
