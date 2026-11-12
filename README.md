# Flask Personal Website & Admin Portal

A Flask-based web application featuring a personal portfolio website with an admin panel for managing contact messages.

## Features

- 🏠 **Home Page**: Personal introduction with user profile
- 📝 **About Page**: Team member information and details
- 💼 **Services Page**: List of services with pricing
- 📧 **Contact Form**: Visitor message submission with SQLite database storage
- 🔐 **Admin Portal**: Secure login system to manage contact messages
  - View all submitted messages
  - Edit message details
  - Delete messages
  - Logout functionality
- 🛡️ **Security**: Password hashing with werkzeug security

## Tech Stack

- **Backend**: Flask
- **Database**: SQLite
- **Template Engine**: Jinja2
- **Security**: werkzeug password hashing
- **Environment**: python-dotenv for configuration

## Requirements

- Python 3.14+
- Flask
- python-dotenv
- werkzeug

## Installation

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

5. Run the application:
```bash
python app.py
```

The application will start on `http://localhost:5431`

## Project Structure

```
flask/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── messages.db           # SQLite database (auto-created)
├── routes/
│   └── api/              # API endpoints
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS, images)
└── tests.py              # Test suite
```

## Routes

### Public Routes
- `GET /` - Home page
- `GET /about` - About page with team information
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
ADMIN_PASSWORD_HASH=your-hashed-password
```

## Database

The application uses SQLite with a `messages` table:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Visitor name |
| email | TEXT | Visitor email |
| message | TEXT | Message content |

## Testing

Run the test suite:
```bash
python -m pytest tests.py -v
```

## API Endpoints

API routes are registered under `/api` prefix. Check `routes/api/` for specific endpoints.

## License

MIT

## Author

Created by Valerii (Engineer)

---

For issues or contributions, please submit a pull request or open an issue.
