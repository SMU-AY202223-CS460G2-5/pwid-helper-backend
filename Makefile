.PHONY: clean-pyc

help:
	@echo "    init"
	@echo "        Initializes project requirements"
	@echo "    shell"
	@echo "        Enters Python virtual environment"
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    test"
	@echo "        Run pytest"
	@echo "    dev"
	@echo "        Runs application in dev mode."

init:
	@./scripts/init

shell:
	@pipenv shell

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
	@rm -rf test-results

lint:
	@./scripts/lint

test:
	@./scripts/test

dev:
	@./scripts/dev
