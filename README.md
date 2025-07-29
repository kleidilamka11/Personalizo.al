# Personalizo.al

This repository contains a simple demo project with a Python backend and a React frontend.

## Folder Overview

- **`backend/`** – FastAPI project with authentication endpoints and unit tests.
- **`frontend/`** – Create React App project with a sample component and tests.

## Installing Dependencies

### Python (backend)

Use a virtual environment and install packages from `backend/requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

After installing the dependencies, apply the database migrations so that the
SQLite schema is up to date:

```bash
cd backend
alembic upgrade head
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

## Email Configuration

Account verification and password reset emails are sent using SMTP. Configure the
following environment variables (e.g. in a `.env` file) for real email delivery:

- `SMTP_HOST` – SMTP server hostname
- `SMTP_PORT` – SMTP server port (default `587`)
- `SMTP_USER` – username for SMTP authentication
- `SMTP_PASSWORD` – password for SMTP authentication
- `EMAIL_FROM` – address used as the "from" field

If `SMTP_HOST` is not set, emails are printed to the console instead. This
allows tests to run without an email server.
