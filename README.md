# Flask Personal Website & Admin Portal

A Flask-based web application featuring a personal portfolio website with an admin panel for managing contact messages.

## Features

- 🏠 **Home Page**: Personal introduction with user profile
- 📝 **About Page**: Team members loaded from PostgreSQL, with filtering, sorting, search and a form to add new employees
- 💼 **Services Page**: List of services with pricing
- 📧 **Contact Form**: Visitor message submission stored in PostgreSQL
- 🔐 **Admin Portal**: Secure login system to manage contact messages
  - View all submitted messages
  - Edit message details
  - Delete messages
  - Logout functionality
- 🛡️ **Security**: Password hashing with werkzeug security

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.14 |
| Web framework | Flask 3.0 |
| Templating | Jinja2 |
| Frontend | HTML, CSS, vanilla JavaScript |
| Database | PostgreSQL 17 |
| DB driver | psycopg 3 (`psycopg[binary]`) |
| Security | Werkzeug password hashing |
| Configuration | python-dotenv |
| Containers | Docker, Docker Compose |
| Testing | pytest, pytest-cov |
| Linting | flake8 |
| CI | GitHub Actions (with a PostgreSQL service container) |
| Dependency management | pip (`requirements.txt`) / uv (`pyproject.toml`, `uv.lock`) |

## Quick Start with Docker

Requires Docker with Compose v2.

```bash
cp .env.example .env     # then set SECRET_KEY and ADMIN_PASSWORD_HASH
docker compose up --build
```

The app is available at `http://localhost:5431`. PostgreSQL runs in the `db`
service, its data is kept in the `pgdata` volume, and the `messages` and `employees`
tables are created automatically on startup. The database is also published on
`127.0.0.1:5433` (change with `POSTGRES_PORT`).

Useful commands:
```bash
docker compose logs -f web                    # follow app logs
docker compose exec db psql -U flask          # open a psql shell
docker compose exec web python -m pytest tests.py -v   # run tests
docker compose down                           # stop (keeps data)
docker compose down -v                        # stop and delete the database volume
```

> **Note:** the test suite truncates the `messages` and `employees` tables of the database in
> `DATABASE_URL`. Don't run it against a database holding messages you want to keep.

> **Note:** wrap `ADMIN_PASSWORD_HASH` in single quotes in `.env`. The hash
> contains `$` characters, which Docker Compose would otherwise treat as variables.

## Local Installation (without Docker)

Requires Python 3.14+ and a running PostgreSQL instance (for example
`docker compose up -d db`).

1. Clone the repository:
```bash
git clone <repository-url>
cd flask
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Make sure `DATABASE_URL` in `.env` points to your PostgreSQL instance, then run the application:
```bash
python app.py
```

The application will start on `http://localhost:5431`

## Project Structure

```
flask/
├── app.py                 # Main Flask application
├── db.py                  # PostgreSQL connection helper
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata (uv)
├── Dockerfile             # Web app image
├── docker-compose.yml     # Web app + PostgreSQL services
├── .env                   # Environment configuration (not committed)
├── .env.example           # Example environment configuration
├── routes/
│   └── api.py             # API endpoints (employees)
├── templates/             # Jinja2 HTML templates
├── static/                # CSS and JavaScript (employee directory, theme)
├── tests.py               # Test suite (requires PostgreSQL)
└── .github/workflows/     # CI: lint + tests against PostgreSQL
```

## Routes

### Public Routes
- `GET /` - Home page
- `GET /about` - About page with team members loaded from the database
- `GET /contact` - Contact form page
- `POST /contact` - Submit contact message
- `GET /services` - Services listing page
- `GET /index` - Index page

### Admin Routes
- `GET /admin/login` - Login page
- `POST /admin/login` - Process login
- `GET /admin/messages` - View all messages (requires login)
- `POST /admin/messages/<id>/delete` - Delete a message (requires login)
- `GET /admin/messages/<id>/edit` - Edit message form (requires login)
- `POST /admin/messages/<id>/edit` - Update message (requires login)
- `POST /admin/logout` - Logout (requires login)

## Admin Login

Default credentials (configure in `.env`):
- **Username**: `admin`
- **Password**: (hashed password stored in `ADMIN_PASSWORD_HASH`)

## Environment Variables

```
SECRET_KEY=your-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH='your-hashed-password'

# PostgreSQL (used by docker compose)
POSTGRES_USER=flask
POSTGRES_PASSWORD=flask
POSTGRES_DB=flask

# Only needed when running the app outside Docker
DATABASE_URL=postgresql://flask:flask@localhost:5433/flask
```

Inside Docker Compose, `DATABASE_URL` is set automatically to point at the `db` service.

## Database

The application uses PostgreSQL. Tables are created on startup, and the `employees`
table is seeded with five default employees the first time it is empty.

**`messages`**:

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | TEXT | Visitor name |
| email | TEXT | Visitor email |
| message | TEXT | Message content |

**`employees`**:

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | TEXT | Employee name |
| age | INTEGER | Age (> 0) |
| position | TEXT | Job position |
| salary | NUMERIC(10,2) | Hourly salary (>= 0) |

## Testing

The tests need a running PostgreSQL database (`DATABASE_URL`). With Docker:
```bash
docker compose exec web python -m pytest tests.py -v
```

Or locally, with the database running (`docker compose up -d db`):
```bash
python -m pytest tests.py -v
```

## API Endpoints

API routes are registered under the `/api` prefix.

- `GET /api/employees` - List all employees from the database
- `POST /api/employees` - Add an employee (JSON: `name`, `age`, `position`, `salary`); returns `201` with the saved employee

## License

MIT

## Author

Created by Valerii (Engineer)

---

For issues or contributions, please submit a pull request or open an issue.
