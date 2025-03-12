# Variables
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
FLASK_APP=app.py
FLASK_ENV=development

# Create a virtual environment and install dependencies
setup:
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Run the Flask app
run:
	$(PYTHON) $(FLASK_APP)

# Initialize the database
init-db:
	$(PYTHON) -c "from app import db, app; app.app_context().push(); db.create_all(); print('Database initialized.')"


# Clean up (remove virtual environment)
clean:
	rm -rf $(VENV) __pycache__

# Help menu
help:
	@echo "Available commands:"
	@echo "  make setup     - Set up virtual environment and install dependencies"
	@echo "  make run       - Run the Flask app"
	@echo "  make init-db   - Initialize the SQLite database"
	@echo "  make clean     - Remove virtual environment and caches"
