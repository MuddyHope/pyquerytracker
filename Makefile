.PHONY: format lint all

# This target formats your code automatically
format:
	@echo "Formatting code with Black and isort..."
	black .
	isort .

# This target checks your code for linting errors without changing files
lint:
	@echo "Running Flake8..."
	flake8 .
	@echo "Running Black (check-only)..."
	black --check .
	@echo "Running Pylint..."
	pylint pyquerytracker/
	@echo "Linting complete."

# A target to run both format and lint
all: format lint