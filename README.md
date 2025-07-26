# Personalizo.al

This repository contains a simple demo project with a Python backend and a React frontend.

## Folder Overview

- **`backend/`** – FastAPI project with authentication endpoints and unit tests.
- **`frontend/`** – Create React App project with a sample component and tests.

## Installing Dependencies

### Python (backend)

Use a virtual environment and install packages from `backend/requirements.txt`:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node (frontend)

Install Node packages using npm:

```bash
cd frontend
npm install
```

## Running Tests

### Backend tests

From the repository root or the `backend` folder run:

```bash
pytest
```

### Frontend tests

Inside the `frontend` folder run:

```bash
npm test
```

Both commands should execute the respective test suites (`pytest` for Python and `npm test` for React).
