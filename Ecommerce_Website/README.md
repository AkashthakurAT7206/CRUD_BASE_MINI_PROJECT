# ECommerce_Website (Django)

This is a small Django-based e-commerce example project. It contains the following applications:

- `Accounts` — user registration, login, password reset (OTP), profile
- `products` — categories, products, CRUD views and product listing
- `cart` — session/authenticated cart, add/update/remove items, checkout view
- `orders` — order creation, listing, detail and cancellation
- `reviews` — product reviews (templates present)

## Prerequisites

- Python 3.10+ (3.11 recommended)
- pip
- (Optional) virtual environment tool: `venv` or `virtualenv`

## Setup (Windows PowerShell)

1. Open PowerShell in the project root (`Ecommerce_Website`).

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Configure environment variables.

You can either set environment variables in your PowerShell session (temporary) or create a `.env` and use a tool like `python-dotenv` to run commands.

Temporary (PowerShell session):

```powershell
$env:DJANGO_SECRET_KEY = 'replace-with-a-strong-secret'
$env:DJANGO_DEBUG = 'True'
$env:EMAIL_HOST_USER = 'your-email@example.com'
$env:EMAIL_HOST_PASSWORD = 'your-email-password-or-app-password'
```

Or copy `.env.example` to `.env` and edit the values. If you use the `python-dotenv` CLI you can run commands via it (the project includes `python-dotenv` in requirements):

```powershell
copy .env.example .env
# edit .env with your values
python -m dotenv run -- python manage.py migrate
python -m dotenv run -- python manage.py runserver
```

5. Run migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

6. Run the development server:

```powershell
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser.

## Media & Static files

- Uploaded media files are stored in the `media/` directory (controlled by `MEDIA_ROOT` in settings).
- Project-level static files can be placed in `static/`. `STATICFILES_DIRS` is configured to include `BASE_DIR/static`.
- For production, run `python manage.py collectstatic` after setting `DJANGO_DEBUG=False` and configuring `STATIC_ROOT` appropriately.

## Notes & Security

- `ecommerce/settings.py` was modified to read `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and email settings from environment variables. Do NOT commit real secrets to the repository.
- An `.env.example` file is included — copy it to `.env` and fill in real values locally.
- If credentials were accidentally committed, rotate them immediately.

## Common commands

```powershell
# activate venv
.\.venv\Scripts\Activate.ps1
# run migrations
python manage.py migrate
# create superuser
python manage.py createsuperuser
# run tests (if any added)
python manage.py test
# run server
python manage.py runserver
```

## Developing further

- Add tests for models and critical views.
- Add CI (GitHub Actions) for linting and running tests.
- Consider stricter production settings: set `ALLOWED_HOSTS`, disable debug, and use a secure secrets manager.

## Contact / Contributors

This repository was scanned and lightly corrected (import bug and settings hard-coded secrets) by an automated assistant. See commit history for changes.
