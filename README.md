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

The development server runs on port `8001`. Start it with:

```bash
npm start
```
and open [http://localhost:8001](http://localhost:8001) in your browser.

The API base URL is configurable via a `.env` file inside `frontend/`. Set
`REACT_APP_BACKEND_BASE_URL` to the backend address before starting the
development server. See `frontend/.env.example` for the default value.

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

## Admin Interface

If you log in as a user with `is_admin` set to `true`, the navigation now exposes links to view all orders and upload finished songs.  The new pages are available at `/admin/orders` and `/admin/upload`.

When a user registers for an account, the backend immediately emails a verification link to the provided address.

## Email Configuration

Account verification and password reset emails are sent using SMTP. Configure the
following environment variables (e.g. in a `.env` file) for real email delivery:

- `SMTP_HOST` – SMTP server hostname
- `SMTP_PORT` – SMTP server port (default `587`)
- `SMTP_USER` – username for SMTP authentication
- `SMTP_PASSWORD` – password for SMTP authentication
- `EMAIL_FROM` – address used as the "from" field
- `LEMONSQUEEZY_API_KEY` – API key for Lemon Squeezy checkouts
- `LEMONSQUEEZY_STORE_ID` – your Lemon Squeezy store ID

If `SMTP_HOST` is not set, emails are printed to the console instead. This
allows tests to run without an email server.

## Rate Limiting

The API now uses Redis to store rate limiting counters. Set the `REDIS_URL`
environment variable to point to your Redis instance (defaults to
`redis://localhost:6379/0`). Ensure Redis is running before starting the
backend server.

The allowed CORS origins are also configurable. Set `ALLOWED_ORIGINS` to a
comma-separated list of origins (or `*` to allow any origin) when launching the
backend.
