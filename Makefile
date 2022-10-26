install:
	poetry install
lint:
	poetry run flake8 tgbot
selfcheck:
	poetry check
check: selfcheck lint
setup: install build package-install