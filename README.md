# Ishflow

> A platform where you can find your dream job... or your dream employee

---

## 📋 Prerequisites

- [Docker](https://docs.docker.com/engine/install/) (for local development)
- [UV](https://docs.astral.sh/uv/getting-started/installation/) (for local Python development)

---

## 🛠️ Local Development Setup

### 1. Python Environment Setup

Create and sync a UV virtual environment:

```bash
uv sync
```

### 2. Install Pre-commit Hooks

```bash
pre-commit install
# or
uv run pre-commit install
```

## 🚀 Local Development Spin Up

### 1. Environment Configuration

Copy the development environment file:

```bash
cp .env.local .env
```

### 2. Start All Services with Docker Compose

```bash
# To Run API/Database/S3/Cache Containers
make compose-up
```

This will start:
- Django application (local development mode)
- PostgreSQL database
- Redis cache
- Minio Storage
- Mailpit (local SMTP server)

### Access Local Services

- **Redoc**: http://localhost:8000/api/v1/docs
- **Swagger**: http://localhost:8000/api/v1/swagger

---

### To create a new Django App

```bash
python manage.py createapp <app_name>
```
Note: [Check this out](./src/apps/shared/management/commands/createapp.py)

### To generate test users
```bash
python manage.py create_test_users
```
Note: [Check this out](./src/apps/accounts/management/commands/create_test_users.py)
