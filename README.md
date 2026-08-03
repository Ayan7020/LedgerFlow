# LedgerFlow

LedgerFlow is a Khata (ledger) management backend built with FastAPI.

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL 17 |
| Migrations | Alembic |
| Validation & settings | Pydantic, pydantic-settings |
| Authentication | Google OAuth (google-auth), PyJWT, bcrypt |
| Logging | Loguru |
| Observability | OpenTelemetry (FastAPI, SQLAlchemy, logging exporters) |
| Package management | uv |
| Containerization | Docker, Docker Compose |

## Prerequisites

Before setting up the project locally, ensure the following are installed:

- **Git** — to clone the repository
- **Python 3.12+** — matches `.python-version`
- **uv** — recommended for dependency management ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Docker** and **Docker Compose** — to run PostgreSQL locally
- **Google Cloud OAuth credentials** — a Client ID for Google Sign-In (`GOOGLE_CLIENT_ID`)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/LedgerFlow.git
cd LedgerFlow
```

### 2. Install dependencies

Using uv (recommended):

```bash
uv sync
```

This reads `pyproject.toml` and `uv.lock` and installs all project dependencies into a virtual environment managed by uv.

### 3. Configure environment variables

Create a `.env` file in the project root. The application and Alembic both load this file at startup.

```env
env="dev"

# Logging / observability (required by config; used in production)
better_stack_source_token="<your-better-stack-token>"
better_stack_host="<your-better-stack-host>"

# Authentication
GOOGLE_CLIENT_ID="<your-google-oauth-client-id>"
SECRET_KEY="<generate-a-secure-random-string>"

# Database (must match Docker Compose and migration settings)
db_username="<db-user>"
db_password="<db-password>"
db_name="ledgerflow_dev"
db_host="localhost"
db_port=5439
```

| Variable | Description |
|----------|-------------|
| `env` | Runtime environment: `dev`, `test`, or `prod` |
| `better_stack_source_token` | Better Stack log source token (used when `env=prod`) |
| `better_stack_host` | Better Stack ingestion host (used when `env=prod`) |
| `GOOGLE_CLIENT_ID` | Google OAuth 2.0 Client ID for sign-in |
| `SECRET_KEY` | Secret used to sign JWT access tokens |
| `db_username` | PostgreSQL username |
| `db_password` | PostgreSQL password |
| `db_name` | PostgreSQL database name |
| `db_host` | Database host (`localhost` when using Docker Compose locally) |
| `db_port` | Database port (`5439` maps to the Compose service) |

Do not commit `.env` to version control. It is listed in `.gitignore`.

### 4. Start PostgreSQL with Docker Compose

From the project root:

```bash
docker compose up -d
```

This starts a PostgreSQL 17 container (`postgres_ledgerflow`) on port **5439**, with credentials and database name taken from your `.env` file.

Verify the container is healthy:

```bash
docker compose ps
```

To stop the database:

```bash
docker compose down
```

To stop and remove persisted data:

```bash
docker compose down -v
```

### 5. Run database migrations

Alembic applies schema changes against the database configured in `.env`. Run migrations with uv:

```bash
uv run alembic upgrade head
```

To create a new migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe your change"
uv run alembic upgrade head
```

### 6. Run the application

Start the FastAPI server with Uvicorn:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is available at `http://localhost:8000`.

Interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 7. Verify the setup

1. Confirm PostgreSQL is running: `docker compose ps`
2. Open `http://localhost:8000/docs` and confirm the API loads
3. Test the auth endpoint: `POST /api/v1/auth/google` with a valid Google OAuth token

## Project Structure

```
LedgerFlow/
├── app/
│   ├── api/v1/          # API routes and dependencies
│   ├── core/            # Config, logging, security, observability
│   ├── db/              # SQLAlchemy engine, session, base models
│   ├── models/          # Database and HTTP request/response models
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic
│   └── main.py          # Application entry point
├── alembic/             # Database migration scripts
├── docker-compose.yaml  # Local PostgreSQL service
├── pyproject.toml       # Project metadata and dependencies
└── uv.lock              # Locked dependency versions
```

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/google` | Authenticate with a Google OAuth token; returns a JWT access token and sets a refresh token cookie |

## Development Notes

- **Environment**: Set `env=dev` for local development. Production mode (`env=prod`) enables Better Stack logging and OpenTelemetry instrumentation.
- **Database port**: The Compose file maps host port `5439` to container port `5432`. Keep `db_port=5439` in `.env` when connecting from the host.
- **Refresh token cookie**: In development, the refresh token cookie is set with `secure=False`. Use HTTPS and `secure=True` in production deployments.