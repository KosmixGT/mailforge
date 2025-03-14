SERVICES := server auth delivery history mailing

.PHONY: lint
lint:
	@for service in $(SERVICES); do \
		echo "Linting $$service..."; \
		black services/$$service/app server/app; \
		flake8 services/$$service/app server/app; \
		mypy services/$$service/app server/app; \
	done

.PHONY: format
format:
	@for service in $(SERVICES); do \
		echo "Formatting $$service..."; \
		black services/$$service/app server/app; \
	done

.PHONY: install-dev
install-dev:
	pip install flake8 black mypy pre-commit
	pre-commit install
