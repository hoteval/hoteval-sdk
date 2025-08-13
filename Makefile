.DEFAULT_GOAL := help

# Check that uv is installed
.PHONY: .uv
.uv:
	@uv --version || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

# Check that pre-commit is installed
.PHONY: .pre-commit
.pre-commit:
	@pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

.PHONY: help
help:
	@echo "HotEval SDK Development Tasks"
	@echo "============================"
	@echo ""
	@echo "Setup:"
	@echo "  install           Install all dependencies and pre-commit hooks"
	@echo "  install-python    Install Python SDK in development mode"
	@echo ""
	@echo "Python SDK:"
	@echo "  test-python       Run Python tests"
	@echo "  format-python     Format Python code"
	@echo "  lint-python       Lint Python code"
	@echo "  typecheck-python  Type check Python code"
	@echo "  clean-python      Clean Python build artifacts"
	@echo "  build-python      Build Python package"
	@echo ""
	@echo "Release (Python):"
	@echo "  release-python    Prepare Python SDK release (requires VERSION=x.y.z)"
	@echo "  release-push      Create PR and release draft"
	@echo ""
	@echo "Examples:"
	@echo "  example-python    Run Python example"
	@echo ""
	@echo "General:"
	@echo "  validate-schema   Validate message schema"
	@echo "  clean             Clean all build artifacts"
	@echo "  all               Run format, lint, and test for all languages"

# Setup targets
.PHONY: install
install: .uv .pre-commit install-python
	@echo "✓ Development environment ready"

.PHONY: install-python
install-python: .uv
	cd python && uv sync --frozen
	cd python && uv pip install -e .

# Python SDK targets
.PHONY: test-python
test-python: .uv
	cd python && uv run pytest tests/ -v

.PHONY: format-python
format-python: .uv
	cd python && uv run ruff format hoteval/
	cd python && uv run ruff check --fix hoteval/

.PHONY: lint-python
lint-python: .uv
	cd python && uv run ruff check hoteval/
	cd python && uv run ruff format --check --diff hoteval/

.PHONY: typecheck-python
typecheck-python: .uv
	cd python && uv run mypy hoteval/

.PHONY: build-python
build-python: .uv
	cd python && uv build

.PHONY: clean-python
clean-python:
	cd python && rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find python -name "__pycache__" -type d -exec rm -rf {} +

# Release targets
.PHONY: release-python
release-python: .uv
	@if [ -z "$(VERSION)" ]; then echo "Usage: make release-python VERSION=x.y.z"; exit 1; fi
	cd python && uv run scripts/release/prepare.py $(VERSION)

.PHONY: release-push
release-push: .uv
	cd python && uv run scripts/release/push.py

# Example targets
.PHONY: example-python
example-python:
	@echo "Setting up demo environment variables..."
	@export HOTEVAL_API_KEY="demo_key" && \
	export HOTEVAL_BASE_URL="http://localhost:8000" && \
	python examples/basic_usage.py

# General targets
.PHONY: validate-schema
validate-schema:
	@echo "Validating message schema..."
	@python -c "import json; json.load(open('schemas/messages.json'))" && echo "✓ Schema is valid JSON"

.PHONY: clean
clean: clean-python
	rm -rf .DS_Store

# Development shortcuts
.PHONY: dev
dev: install
	@echo "✓ Development environment ready"

.PHONY: check
check: test-python lint-python typecheck-python validate-schema
	@echo "✓ All checks passed"

.PHONY: all
all: format-python lint-python typecheck-python test-python
	@echo "✓ All tasks completed"