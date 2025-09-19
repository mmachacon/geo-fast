# geo-fast

A FastAPI-based project for geospatial operations and API services.

## Project Decisions

## Architectural Decisions

- **Modular Structure:**

  - The project is organized with a clear separation of concerns:
    - `main.py` initializes the FastAPI app and includes the root application logic.
    - The `src/` directory contains:
      - `models.py`: Defines data models and schemas for request/response validation.
      - `routes.py`: Contains API route definitions, keeping endpoints organized and maintainable.
      - `utils.py`: Utility functions for shared logic, promoting code reuse.
      - `test.py`: Localized tests for individual modules.
      - `__init__.py`: Ensures the directory is treated as a package, supporting imports.

- **Separation of Concerns:**

  - Business logic, data models, and API routes are kept in separate files to improve maintainability and testability.
  - This structure allows for easy scaling as new features or endpoints are added.

- **Scalability & Extensibility:**

  - New routes or models can be added to the `src/` directory without affecting the core application logic in `main.py`.
  - Utilities are centralized in `utils.py` to avoid duplication and simplify updates.

- **Testing Strategy:**

  - `pytest` is used for both unit and integration tests.
  - Tests are placed in `test_app.py` (for app-level tests) and `src/test.py` (for module-level tests), supporting a layered testing approach.

- **Environment Management:**

  - Python 3.12 is recommended for compatibility and performance.
  - Virtual environments are used to isolate dependencies and prevent conflicts.

- **Version Control:**
  - `.gitignore` is configured to exclude cache files, environment files, and IDE-specific files, keeping the repository clean.

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mmachacon/geo-fast.git
   cd geo-fast
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   or
    fastapi run main.py
   ```
   - The API will be available at `http://127.0.0.1:8000`.
   - Interactive docs: `http://127.0.0.1:8000/docs`

## Running Tests

To run all tests, use:

```bash
pytest
```

You can run specific test files, for example:

```bash
pytest test_app.py
pytest src/test.py
```

For more verbose output, add the `-v` flag:

```bash
pytest -v
```

To see test coverage (if `pytest-cov` is installed):

```bash
pytest --cov=src
```

## Additional Notes

- All source code is in the `src/` directory for clarity.
- Configuration and environment variables can be set in `.env` (add to `.gitignore`).
- For database support, update `requirements.txt` and add connection details in `main.py` or `src/utils.py`.

## Contact

For questions or contributions, open an issue or pull request on GitHub.
