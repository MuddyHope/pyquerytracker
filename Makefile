.PHONY: lint

lint:
	@echo "Running code formatters and linters..."
	# Format code
	black .
	isort .
	# Run linters
	flake8 .
	pylint pyquerytracker/
	@echo "Linting complete." 