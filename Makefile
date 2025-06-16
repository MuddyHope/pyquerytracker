.PHONY: lint

lint:
	@echo "Running Flake8..."
	flake8 pyquerytracker/

	@echo "Running Black (check-only)..."
	black --check pyquerytracker/

	@echo "Running Pylint..."
	pylint pyquerytracker/
