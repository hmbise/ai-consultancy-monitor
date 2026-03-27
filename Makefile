# AI Consultancy Monitor - Makefile
# Usage: make <command>

.PHONY: dev install test format lint save watch commit

# Default Python
PYTHON := python

# Install dependencies
install:
	pip install -e ".[dev]"

# Run development server with auto-reload
dev:
	uvicorn src.api.main:app --reload

# Run tests
test:
	pytest -v

# Format code
format:
	black src tests
	ruff check --fix src tests

# Lint code
lint:
	ruff check src tests
	mypy src

# Quick save - auto-commit all changes with timestamp
save:
	@git add -A
	@git commit -m "checkpoint: $(shell date +%Y-%m-%d-%H:%M)" || echo "Nothing to commit"
	@echo "✓ Saved at $(shell date +%H:%M)"

# Commit with custom message (usage: make commit MSG="your message")
commit:
	@git add -A
	@git commit -m "$(MSG)" || echo "Nothing to commit"

# Auto-commit every 5 minutes (run in separate terminal)
watch:
	@echo "Starting auto-commit watcher (5 min intervals)..."
	@echo "Press Ctrl+C to stop"
	@while true; do \
		sleep 300; \
		if [ -n "$$(git status --porcelain 2>/dev/null)" ]; then \
			git add -A && git commit -m "auto: $$(date +%Y-%m-%d-%H:%M)" && echo "Committed at $$(date +%H:%M)"; \
		fi; \
	done

# Setup development environment (first time)
setup:
	$(PYTHON) -m venv .venv
	@echo "Run: .venv\Scripts\activate (Windows) or source .venv/bin/activate (Mac/Linux)"
	@echo "Then run: make install"

# Database initialization
init-db:
	$(PYTHON) -c "import asyncio; from src.core.database import init_db; asyncio.run(init_db())"
	@echo "Database schema initialized"

# Start worker
worker:
	celery -A src.worker worker -l info

# Start beat scheduler
beat:
	celery -A src.worker beat -l info

# Docker services
docker-up:
	docker-compose up -d redis elasticsearch

docker-down:
	docker-compose down

# Full stack (docker + api + worker)
stack:
	make docker-up
	@echo "Starting API and worker..."
	@start cmd /k "make dev"
	@start cmd /k "make worker"
