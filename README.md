# FastAPI ERP Platform Foundation

A production-oriented FastAPI foundation for an enterprise ERP platform built around a modular architecture, clear dependency boundaries, and validation-first request handling.

## What is included

- Clean application entrypoint with FastAPI factory pattern
- Modular user domain with repository, service, schema, validator, and API layers
- Structured exception handling and logging
- Role-based access checks for administrative operations
- Regression tests covering user creation, duplicate prevention, and access control

## Project structure

```text
app/
├── core/
│   ├── exceptions.py
│   ├── logging.py
│   └── security.py
├── modules/
│   └── users/
│       ├── api.py
│       ├── dependencies.py
│       ├── models.py
│       ├── repositories.py
│       ├── schemas.py
│       ├── services.py
│       └── validators.py
└── main.py
main.py
requirements.txt
tests/
└── test_users.py
```

## Run locally

```bash
./.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

## API endpoints

- POST /api/v1/users/ - create a user
- GET /api/v1/users/ - list users (admin only)
- GET /health - health check

## Example request

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "StrongPass123!",
    "full_name": "Admin User",
    "role": "admin"
  }'
```

## Testing

```bash
./.venv/Scripts/python.exe -m unittest discover -s tests -v
```

## Notes

The current implementation is a solid foundation for a larger ERP platform. The user module demonstrates the architecture pattern that should be repeated for modules such as customers, products, inventory, orders, and finance.
