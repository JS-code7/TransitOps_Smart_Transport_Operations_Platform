# TransitOps Backend

Django REST Framework backend for the TransitOps frontend.

## Features

- JWT-free token auth using DRF tokens
- CRUD endpoints for vehicles, drivers, trips, maintenance, fuel logs, expenses, notifications, and settings
- Collection sync endpoints used by the frontend snapshot writer
- MySQL support via `PyMySQL`
- CORS configured for the Vite frontend

## Setup

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Copy `.env.example` to `.env` and configure database credentials.
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Seed demo data:
   ```bash
   python manage.py seed_demo_data
   ```
5. Start the API:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## API Prefix

All API routes are mounted under `/api/`.
